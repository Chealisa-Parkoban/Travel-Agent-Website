//
// show the image
function showImg() {
    var fileInput = document.querySelector('input[type=file]'),
        previewImg = document.querySelector('#img');
        console.log(previewImg)


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


// // 显示图片
//     $("#intro_pic").on("change",function() {
//         let filePath = $(this).val();//读取图片路径
//
//         let fr = new FileReader();//创建new FileReader()对象
//         let imgObj = this.files[0];//获取图片
//         fr.readAsDataURL(imgObj);//将图片读取为DataURL
//
//         if(filePath.indexOf("jpg") !== -1 || filePath.indexOf("JPG") !== -1 || filePath.indexOf("PNG") !== -1 || filePath.indexOf("png") !== -1) {
//             fr.onload = function() {
//                 $("#pic").attr('src',this.result);
//             };
//         }
//     });

