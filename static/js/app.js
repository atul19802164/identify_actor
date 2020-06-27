Dropzone.autoDiscover = false;

function init() {
	var actorName = document.getElementById("actorName");
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
       
        var url = "https://identifyactor.herokuapp.com/classify_image";
	
        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
			if(data.length>0){
				 $("#actorName").show();
			}
    $("#actorName").html("<h2>" + data[0].class.toString()+"</h2>");                  
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    $("#actorName").hide();
    init();
});
