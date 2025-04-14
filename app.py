import argparse
from lucene import initVM
from org.apache.lucene.store import FSDirectory
from java.io import File
from org.apache.lucene.index import DirectoryReader

def main():
    parser = argparse.ArgumentParser(description='Lucene index reader')
    parser.add_argument('index_path', help='Path to the Lucene index directory')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum number of documents to display (default: 10)')
    args = parser.parse_args()

    initVM(vmargs=['--add-modules=jdk.incubator.vector'])

    index_path = File(args.index_path).toPath()
    directory = FSDirectory.open(index_path)

    print(f"Index directory opened successfully at: {index_path}")

    try:
        reader = DirectoryReader.open(directory)
        
        num_docs = reader.numDocs()
        max_doc = reader.maxDoc()
        display_limit = min(args.limit, max_doc)
        
        print(f"Index contains {num_docs} documents")
        print(f"Total docs (including deleted): {max_doc}")
        print(f"Displaying first {display_limit} documents:")
        
        for i in range(display_limit):
            doc = reader.document(i)
            print(f"\nDocument {i}:")
            for field in doc.getFields():
                print(f"{field.name()}: {field.stringValue()}")
    
    finally:
        if 'reader' in locals():
            reader.close()

if __name__ == "__main__":
    main()