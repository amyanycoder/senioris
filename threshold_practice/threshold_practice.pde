PImage img;
float thresholdValue = 0.0;

void setup(){
   background(255);
   
    size(756, 1008);
    background(255);
    img = loadImage("patch.jpg");
    img.resize(0, 1008);
}

void draw(){
  image(img,0,0);
  filter(THRESHOLD, thresholdValue);
  
}

//increases the threshold value everytime the mouse is clicked.
void mouseClicked(){
   if(thresholdValue >= 1){
       thresholdValue = 0; 
   }
   else{
     thresholdValue += 0.05;
   }
}
