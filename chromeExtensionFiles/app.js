var express = require('express');
var path = require('path');
var PythonShell = require('python-shell');


var app = express();

app.use('/hello',function(request,response){
    console.log("here");
    // var options = {
    //     mode: 'json',
    //     args: "hi"
    // };
    // PythonShell.run('C:\\Users\\il675252\\Desktop\\third year\\מחט בערימת דאטה\\visitedUrls\\app.py',options, function(err, res){
    //     if(err)
    //     {
    //         alert("here");
    //     }
    //     else
    //     {
    //         alert("here");
    //     }
    // })
});

app.listen(8080, function () {
    console.log('Example app listening on port 3000!')
});

