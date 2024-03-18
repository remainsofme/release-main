

let current_index=0;
const uploading_pic=document.getElementById('pic')
const input_field=document.getElementById('input_field')
const previous=document.getElementById('previous')
const next=document.getElementById('next')
const submit=document.getElementById('submit')
const annotation_element=document.getElementById('exampleFormControlTextarea1')
const progressing_bar=document.getElementById('progressing')



async function upload(){
    uploading_pic.src='/static/pictures/uploading.gif'
    input_field.disabled=true
    previous.disabled=true
    next.disabled=true
    submit.disabled=true
    console.log(input_field.files);
    const form_data=new FormData();
    for (const file of input_field.files){
        form_data.append('my_files',file);
        console.log('!!');
    }
    console.log(form_data)
    const response= await fetch('/gallery_maker',{
        method:'POST',
        body:form_data
    })
    const data=await response.json()
    console.log(data)
    picture_data=data
    display_image(current_index)
    input_field.disabled=false
    previous.disabled=false
    next.disabled=false
    submit.disabled=false    
}


function annotation(index){
    if (annotation_element.value==''){
        //pass
    }
    else {
        picture_data[index][2]=paragraph(annotation_element.value,25);
        annotation_element.value='';
        console.log(picture_data);
    }
}

function display_image(index){
    submit.disabled=true
    previous.disabled=true
    next.disabled=true
    const prefix_string='/static/image/';
    console.log(index)
    uploading_pic.src=prefix_string+picture_data[index][1];
    console.log(prefix_string+picture_data[index][0]);
    submit.disabled=false
    previous.disabled=false
    next.disabled=false
}

function next_image(){
    annotation(current_index);
    current_index=(current_index+1)%picture_data.length;
    display_image(current_index);
    annotation_element.value=picture_data[current_index][2];
    console.log(current_index);
}

function previous_image(){
    annotation(current_index);
    if (current_index>0){
        current_index=(current_index-1)%picture_data.length;
        console.log(current_index);
        display_image(current_index);
        annotation_element.value=picture_data[current_index][2];
    }
    else if (current_index<=0){
        current_index=picture_data.length-(-1*(current_index-1));
        console.log(current_index);
        display_image(current_index)
        annotation_element.value=picture_data[current_index][2];
    }
}

function paragraph(text,interval){
    let text_para=''
    for (let i=0;i<text.length;i+=interval){
        text_para+=text.slice(i,i+interval)+'\n'
    }
    return text_para
}

function submit_function(){
    progressing()
    submit.disabled=true
    previous.disabled=true
    next.disabled=true
    input_field.disabled=true
    annotation(current_index)
    fetch('/gallery_maker',{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(picture_data)

    }
    )
};

function progressing(){
    progressing_bar.src='/static/pictures/giphy.gif'
}
function stop(){
    progressing_bar.src=''
    input_field.disabled=false
        submit.disabled=true
        previous.disabled=true
        next.disabled=true
    
}

function download_file(){
    download_link=document.getElementById('download_link')
    download_link.click()
    stop()
    d=document.getElementById('pic')
    d.src='/static/pictures/upload_icon.png'
}

window.onload=function(){
    function preloadGIF(url) {
        const image = new Image();
        image.src = url;
    }
    
    // Preload your GIF by passing its URL
    preloadGIF('/static/pictures/giphy.gif');

    
    input_field.addEventListener('change', function() {
    if (input_field.files.length > 0) {
        upload();

        drop_area_text.innerHTML="";
    }
    });
    let next_button=document.getElementById('next');
    next_button.addEventListener('click',next_image)
    let previous_button=document.getElementById('previous');
    previous_button.addEventListener('click',previous_image);
    let submit_button=document.getElementById('submit');
    submit_button.addEventListener('click',
    function (){
        submit_function()
        setTimeout(function(){
            download_file()
            let drop_area_text=document.getElementById('drop_area_text')
            drop_area_text.innerHTML="Drag and drop here<br>to upload an image";
            current_index=0
        },10000
        );
        
    
     
    }
    )
    let drop_area=document.getElementById('drop_area');
    let drop_area_text=document.getElementById('drop_area_text')
    drop_area.addEventListener('drop',function(e){e.preventDefault();
    input_field.files=e.dataTransfer.files
    upload();
    drop_area_text.innerHTML="";
     }
    );
    drop_area.addEventListener('dragover',function(e){e.preventDefault();});


    
    
}