import argparse
from lucene import initVM
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.analysis.standard import StandardAnalyzer

def main():
    parser = argparse.ArgumentParser(description='Lucene index reader by document field ID')
    parser.add_argument('index_path', help='Path to the Lucene index directory')
    parser.add_argument('--limit', type=int, default=10,
                        help='Maximum number of documents to display (default: 10)')
    parser.add_argument('--offset', type=int, default=0,
                        help='Starting document offset (default: 0)')
    parser.add_argument('--doc_ids', type=str, default=None,
                        help='Comma-separated list of values in the "id" field to fetch directly')

    args = parser.parse_args()

    initVM(vmargs=['--add-modules=jdk.incubator.vector'])

    index_path = File(args.index_path).toPath()
    directory = FSDirectory.open(index_path)

    print(f"Index directory opened successfully at: {index_path}")

    try:
        reader = DirectoryReader.open(directory)
        searcher = IndexSearcher(reader)
        analyzer = StandardAnalyzer()

        num_docs = reader.numDocs()
        max_doc = reader.maxDoc()

        print(f"Index contains {num_docs} documents (maxDoc={max_doc})")

        if args.doc_ids:
            id_values = [doc_id.strip() for doc_id in args.doc_ids.split(',') if doc_id.strip()]
            print(f"\nSearching for documents with field 'id' in: {id_values}")
            for doc_id_value in id_values:
                try:
                    query = TermQuery(Term("id", doc_id_value))
                    hits = searcher.search(query, 1).scoreDocs
                    if not hits:
                        print(f"\nNo document found with id = {doc_id_value}")
                        continue
                    doc = searcher.doc(hits[0].doc)
                    print(f"\nDocument with id = {doc_id_value}:")
                    for field in doc.getFields():
                        print(f"{field.name()}: {field.stringValue()}")
                except Exception as e:
                    print(f"\nError retrieving document with id = {doc_id_value}: {str(e)}")

        else:
            start = max(0, min(args.offset, max_doc - 1))
            end = min(start + args.limit, max_doc)
            actual_limit = end - start
            print(f"\nDisplaying {actual_limit} documents starting from offset {start}:")
            for i in range(start, end):
                if reader.hasDeletions() and reader.isDeleted(i):
                    print(f"\nDocument {i} is deleted. Skipping.")
                    continue
                try:
                    doc = reader.document(i)
                    print(f"\nDocument {i}:")
                    for field in doc.getFields():
                        print(f"{field.name()}: {field.stringValue()}")
                except Exception as e:
                    print(f"\nError reading document {i}: {str(e)}")

    finally:
        if 'reader' in locals():
            reader.close()

if __name__ == "__main__":
    main()
