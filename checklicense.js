var firstPoint, secondPoint;

// Prompt for the user for the first point
var options = new Acad.PromptPointOptions("Specify the first point of the rectangle: ");
Acad.Editor.getPoint(options).then(onFirstPoint,error);

// If the first point was successful, prompt the user for a second point
function onFirstPoint(arg)
{
   var obj = arg;
   firstPoint = obj.value;

   // Prompt for the user for the second point
   var options = new Acad.PromptPointOptions("Specify the opposite corner of the rectangle: ");
   Acad.Editor.getPoint(options).then(onSecondPoint,error);
}

// If an error occurred, display a general error message
function error()
{
   alert("Invalid point specified.");
}

// If both points were successfully specified, then draw the rectangle
function onSecondPoint(arg)
{
   var obj = arg;
   secondPoint = obj.value;

   // Draw the rectangle
   Acad.Editor.executeCommand("RECTANG", firstPoint.x + "," + firstPoint.y, "", secondPoint.x + "," + secondPoint.y);
}