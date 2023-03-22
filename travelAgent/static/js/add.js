
// show the image
function showImg() {
    var fileInput = document.querySelector('input[type=file]'),
        previewImg = document.querySelector('img');
    fileInput.addEventListener('change', function () {
        var file = this.files[0];
        var reader = new FileReader();
        // Listen to the onload event of the reader object,
        // and give the base64 encoding to the preview image when the image is loaded.
        reader.addEventListener("load", function () {
            previewImg.src = reader.result;
        }, false);
        // Call the reader.readAsDataURL() method to convert the image to base64
        reader.readAsDataURL(file);
    }, false);
}
