import st7789
from flask import Flask, request, render_template_string
from PIL import Image
import base64
import io

# -----------------------
# TFT DISPLAY SETUP
# -----------------------

disp = st7789.ST7789(
    port=0,
    cs=0,
    dc=24,
    rst=25,
    width=320,
    height=240,
    rotation=0,
    spi_speed_hz=80000000
)

disp.begin()

disp.display(Image.new("RGB",(320,240),(0,0,0)))

# -----------------------
# FLASK SERVER
# -----------------------

app = Flask(__name__)

HTML_PAGE = '''

<!DOCTYPE html>
<html>

<head>
<meta charset="UTF-8">
<title>TFT Image Editor</title>

<link rel="stylesheet" href="https://unpkg.com/cropperjs@1.6.1/dist/cropper.min.css"/>

<style>

body{
font-family: "Segoe UI", sans-serif;
background:#1E1E2F;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
margin:0;
color:white;
}

.container{
display:flex;
gap:50px;
}

.card{
background:#2A2A3D;
padding:30px;
border-radius:20px;
width:460px;
box-shadow:0 20px 40px rgba(0,0,0,0.6);
text-align:center;
}

h2{
color:#E5E5F0;
margin-bottom:20px;
}

.upload-box{
border:2px dashed #6C63FF;
padding:12px;
border-radius:12px;
cursor:pointer;
margin-bottom:20px;
background:#1E1E2F;
}

input[type=file]{
display:none;
}

.editor-container{
width:100%;
height:300px;
background:#111;
border-radius:10px;
overflow:hidden;
display:flex;
align-items:center;
justify-content:center;
margin-bottom:20px;
}

#image{
max-width:100%;
max-height:100%;
}

.controls{
display:flex;
justify-content:center;
gap:12px;
flex-wrap:wrap;
}

button{
padding:10px 18px;
border:none;
border-radius:10px;
background:#6C63FF;
color:white;
font-weight:600;
cursor:pointer;
}

button:hover{
background:#5A52E0;
}

.preview-frame{
width:320px;
height:240px;
margin:auto;
border-radius:12px;
background:black;
border:5px solid #6C63FF;
display:flex;
align-items:center;
justify-content:center;
overflow:hidden;
}

.preview-frame img{
width:100%;
height:100%;
object-fit:cover;
}

.download-btn{
margin-top:25px;
background:#FF8A65;
}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h2>Upload & Edit</h2>

<label class="upload-box">
📁 Select Image
<input type="file" id="imageInput">
</label>

<div class="editor-container">
<img id="image">
</div>

<div class="controls">
<button onclick="zoomIn()">Zoom In</button>
<button onclick="zoomOut()">Zoom Out</button>
<button onclick="cropImage()">Crop for TFT</button>
<button onclick="invertImage()">Invert</button>
<button onclick="sendToTFT()">Display on TFT</button>
</div>

</div>


<div class="card">

<h2>TFT Preview</h2>

<div class="preview-frame">
<img id="result">
</div>

</div>

</div>


<script src="https://unpkg.com/cropperjs@1.6.1/dist/cropper.min.js"></script>

<script>

let cropper;

const image=document.getElementById("image");
const result=document.getElementById("result");

document.getElementById("imageInput").onchange=function(e){

const file=e.target.files[0];
if(!file) return;

const reader=new FileReader();

reader.onload=function(){

image.src=reader.result;

if(cropper) cropper.destroy();

cropper=new Cropper(image,{
aspectRatio:320/240,
viewMode:1,
autoCropArea:1
});

}

reader.readAsDataURL(file);

};


function zoomIn(){ if(cropper) cropper.zoom(0.1); }
function zoomOut(){ if(cropper) cropper.zoom(-0.1); }


function cropImage(){

const canvas=cropper.getCroppedCanvas({
width:320,
height:240
});

result.src=canvas.toDataURL();

}


function invertImage(){

const img=new Image();

img.onload=function(){

const canvas=document.createElement("canvas");
canvas.width=img.width;
canvas.height=img.height;

const ctx=canvas.getContext("2d");

ctx.drawImage(img,0,0);

let data=ctx.getImageData(0,0,canvas.width,canvas.height);

for(let i=0;i<data.data.length;i+=4){

data.data[i]=255-data.data[i];
data.data[i+1]=255-data.data[i+1];
data.data[i+2]=255-data.data[i+2];

}

ctx.putImageData(data,0,0);

result.src=canvas.toDataURL();

};

img.src=result.src;

}


function sendToTFT(){

fetch("/upload",{
method:"POST",
body:JSON.stringify({image:result.src}),
headers:{"Content-Type":"application/json"}
});

}

</script>

</body>
</html>

'''


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/upload", methods=["POST"])
def upload():

    data=request.json["image"]

    image_data=base64.b64decode(data.split(",")[1])

    img=Image.open(io.BytesIO(image_data)).convert("RGB")

    img=img.resize((320,240))

    disp.display(img)

    return "OK"


app.run(host="0.0.0.0",port=5000)
