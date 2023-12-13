function test(){
        var treatment_op = document.getElementById("treatment_op");
        console.log(treatment_op.value)

        var convert_to = document.getElementById("convert_to");
        let image_ops = ["JPEG","JPG","PNG","TIFF"];
        convert_to.disabled = true;

        if(treatment_op.value =="Conversion"){
                convert_to.disabled = false;

                const elements = document.querySelectorAll('.extenType');
                const count = elements.length;

                if(count <= 1){
                        for(var i = 0; i < image_ops.length; i++) {
                                var opt = image_ops[i];
                                var el = document.createElement("option");
                                el.textContent = opt;
                                el.className = "extenType"
                                el.value = opt;
                                convert_to.appendChild(el);
                        }

                        console.log(count)
                }
        }else if(treatment_op.value =="Transcribe"){
                console.log("Hi")
        }
}

function getFileType(file) {

        if(file.type.match('image.*'))
          return 'image';
      
        if(file.type.match('video.*'))
          return 'video';
      
        if(file.type.match('audio.*'))
          return 'audio';
      
        // etc...
      
        return 'other';
      }