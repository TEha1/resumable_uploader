function getFileMd5(file) {
    var dfd = jQuery.Deferred();
    /**
     * reference:
     *    https://github.com/satazor/SparkMD5
     */
    var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
        chunkSize = 2097152,                             // Read in chunks of 2MB
        chunks = Math.ceil(file.size / chunkSize),
        currentChunk = 0,
        spark = new SparkMD5.ArrayBuffer(),
        fileReader = new FileReader();

    fileReader.onload = function (e) {
        dfd.notify('read chunk # ' + (currentChunk + 1) + ' of ' + chunks);
        spark.append(e.target.result);                   // Append array buffer
        currentChunk++;

        if (currentChunk < chunks) {
            loadNext();
        } else {
            dfd.resolve(spark.end());
        }
    };

    fileReader.onerror = function () {
        dfd.reject('oops, something went wrong.');
    };

    var loadNext = function () {
        var start = currentChunk * chunkSize,
            end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;

        fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
    };

    loadNext();

    return dfd.promise();
}

function calculateMd5(blob) {
    var reader = new FileReader();
    reader.readAsBinaryString(blob);
    reader.onloadend = function () {
        let result = reader.result;
        console.log("result = ", blob.arrayBuffer())
        var hash = CryptoJS.alg.MD5(result).toString();
        // or CryptoJS.SHA256(reader.result).toString(); for SHA-2
        console.log("MD5 Checksum", hash);
        return hash
    };
}


$('#image').change(
    function () {
        var reader = new FileReader();
        reader.addEventListener(
            'load',
            function () {
                var wordArray = CryptoJS.lib.WordArray.create(this.result);
                let hexx = CryptoJS.MD5(wordArray).toString();
                console.log("hexx = ", hexx);
                $("#hex").val(hexx);
            }
        );
        reader.readAsArrayBuffer(this.files[0]);
    }
);

// $("#image_form").submit(function (e) {
//     e.preventDefault();
//     let image1 = $("#image")[0].files[0];
//     console.log("image1 = ", image1);
//
//
//     // console.log("has = ", calculateMd5(image1));
//
//
//     // let md5 = CryptoJS.algo.MD5.create();
//     // let image_encode = CryptoJS.enc.Utf8.parse(image1);
//     // console.log('image_encode = ', image_encode);
//     // md5.update(image_encode);
//     // let hash_ = md5.finalize();
//     // let hashHex = hash_.toString();
//     // console.log("hash = ", hash_);
//     // console.log("hashHex = ", hashHex);
//     // var input_ = $("<input>")
//     //     .attr("type", "hidden")
//     //     .attr("name", "hex").val(hashHex);
//     // $('#image_form').append(input_);
//     //
//     // let hash = md5(image1);
//     // console.log("hash = ", hash)
//     //
//     // var spark = new SparkMD5.ArrayBuffer()
//     // spark.append(image1);
//     // let hashHex = spark.end();
//     // console.log("hashHex = ", hashHex);
//     // var input_ = $("<input>")
//     //     .attr("type", "hidden")
//     //     .attr("name", "hex").val(hashHex);
//     // $('#image_form').append(input_);
//     // console.log("hexHash = ", hashHex);
//
//     // let hash = getFileMd5(image1);
//     // console.log(hash)
//
//     $("#image_form").off('submit').submit();
// });
