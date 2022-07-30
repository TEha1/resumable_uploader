import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

digests = {
    "md5": "md5",
    "sha1": "sha1sum",
    "sha224": "sha224sum",
    "sha256": "sha256sum",
    "sha512": "sha512sum",
}

parser = argparse.ArgumentParser(description="CFTH (Compare File To Hash)")
parser.add_argument(
    "digest", help="The hash digest. Valid options: md5, sha1, sha224, sha256, sha512"
)
parser.add_argument("file", help="The file to check")
parser.add_argument("hash", help="The hash to compare against")
args = parser.parse_args()

file_to_hash = Path(args.file)
hash_digest = args.digest.lower()
hash_to_check = args.hash.lower()

if hash_digest not in digests:
    print(
        "First argument is not a valid hash digest, must be md5, sha1, sha224, sha256, sha512."
    )
    sys.exit(1)
elif not file_to_hash.is_file():
    print("Second argument ({}) is not a file.".format(file_to_hash))
    sys.exit(1)
else:
    file_hash = subprocess.run(
        [digests[hash_digest], str(file_to_hash)], stdout=subprocess.PIPE, shell=True
    )
    file_hash = str(file_hash.stdout).split(" ")[0]
    file_hash = file_hash[2:]


print("----------")
print("Hash of file: {}".format(file_hash.lower()))
print("Hash to check: {}".format(hash_to_check))
print("Hashes match: {}".format(file_hash == hash_to_check.lower()))
print("----------")


md5_hash = hashlib.md5()

a_file = open("WWW.YIFY-TORRENTS.COM.jpg", "rb")
content = a_file.read()
md5_hash.update(content.encode("utf-8"))

digest = md5_hash.hexdigest()
print("digest = ", digest)
