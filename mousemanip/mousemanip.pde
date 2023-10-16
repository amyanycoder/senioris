import java.io.*;

String str;
String[] strarray;
int[] intvalues;
PImage img;
int posterizeValue = 30;
boolean inverted = false;

void setup() {
    noStroke();
    size(756, 1008);
    background(255);
    img = loadImage("patch.jpg");
    img.resize(0, 1008);
    //reads a file and copies it into a string
    try{
      str = fileToString();
    }
    catch(Exception e){
      println("file not found.");
    }
    
    strarray = str.split(" ");
    
    intvalues = new int[strarray.length];
    
    for(int i = 0; i < strarray.length; i++){
      for(int j = 0; j < strarray[i].length(); j++){
          intvalues[i] += (int) strarray[i].charAt(j) + 700;
      }
    }
    
}

void draw(){
    mouseWheel();
  
    image(img, 0, 0);
    filter(POSTERIZE, posterizeValue);
    //inverts the image when the left mouse button is clicked
    if(inverted){
      filter(INVERT);
    }
  
    println();
  
    fill(0, 0, 0);    
    
    int rectheight = 1008 / strarray.length;
    
    //draws a rectangle for every word in the string
    for(int i = 0; i < strarray.length; i++){
      
      //only adds the word if it is not blank
      if(!strarray[i].isEmpty()){
        int colorvalue = abs(intvalues[i]);
        //fill(r, g, b, alpha)
        fill((colorvalue  + mouseY) % 256, (colorvalue * 2 + mouseY) % 256, (colorvalue * 3 + mouseY) % 256, (colorvalue * 5 + mouseX) % 256);
        //println(strarray[i] + ": " + colorvalue % 256 + "," + (colorvalue * 2) % 256 + "," + (colorvalue * 3) % 256);
        rect(0, 0 + rectheight * i, 756, rectheight);
      }

    }
    
    //prints the array of strings
    for(int i = 0; i < strarray.length; i++){
       //println(i + ", " + strarray[i]);
    }
}

String fileToString() throws Exception{
    FileReader fr = new FileReader("C:\\Users\\benja\\Documents\\School\\SENIOR IS\\samplesketch\\helloworld.txt");
    String str = "";
    
    int i = 0;
    while((i = fr.read()) != -1){
      str += (char) i;
      
    }
    
    fr.close();
    
    return str;
}

//calls everytime the mousewheel is active
void mouseWheel(MouseEvent event) {
  float e = event.getCount();
  posterize(e);
}

void mouseClicked(){
    inverted = !inverted; 

}


void posterize(float e){
    if(posterizeValue + e > 30){
       posterizeValue = 2; 
    }
    else if(posterizeValue + e < 2){
       posterizeValue = 30; 
    }
    else if(e > 0){
      posterizeValue++;
    }
    else if(e < 0){
      posterizeValue--;
    }
    //println(posterizeValue);

}
