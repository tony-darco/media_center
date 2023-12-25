function test(){
        var treatment_op = document.getElementById("treatment_op");
        console.log(treatment_op.value)

        var convert_to = document.getElementById("convert_to");
        JSON.parse
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

$(document).ready(function(){
    $(service_select).on("change", function(){
        $("#convert_div").hide();
        $("#transcribe_div").hide();

        function check(id){
            return(document.getElementById(id).length <= 1)
        }

        if(this.value == 'convert_image'){
            $("#convert_div").show();
            $(function(){
                var data = ["JPG", "PNG", "BLP", "BMP", "WEBP", "TIFF", "TGA", "SPIDER", "SGI", "PPM", "MSP", "JPEG", "IM", "ICO", "ICNS", "GIF", "EPS", "DIB", "DDS"];
                if (check("convert_select")){
                    $.each(data,function(i, option){
                        $("#convert_select").append($('<option/>').attr("value", option).text(option));
                    })
                }
            })
        }else if(this.value == 'convert_audio'){
            $("#convert_div").show();
            $(function(){
                var data = ["MP3"]
                if (check("convert_select")){
                    $.each(data,function(i, option){
                        $("#convert_select").append($('<option/>').attr("value", option).text(option));
                    })
                }
            })
        }else if(this.value == 'convert_video'){
            $("#convert_div").show();
            $(function(){
                var data = ["MP4","WAV"]
                if (check("convert_select")){
                    $.each(data,function(i, option){
                        $("#convert_select").append($('<option/>').attr("value", option).text(option));
                    })
                }
            })
        }
        else if(this.value == 'transcribe'){
            $("#transcribe_div").show();
            $(function(){
                var data = ["Text File","Text on web page"]
                if (check("transcribe_select")){
                    $.each(data,function(i, option){
                        $("#transcribe_select").append($('<option/>').attr("value", option).text(option));
                    })
                }
            })
        }
    });
});

function search_function() {
    let input = document.getElementById('myInput')
    input.value = input.value.toLowerCase();
    let x = document.getElementsByClassName('supported_class');
   
    for (i = 0; i < x.length; i++) {
      if (!x[i].innerHTML.toLowerCase().includes(input.value)) {
        x[i].style.display = "none";
      }
      else {
        x[i].style.display = "list-item";
      }
    }
}