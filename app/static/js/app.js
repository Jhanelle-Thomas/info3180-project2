// Your JavaScript Code here
var app = angular.module("wishListApp", []);

app.controller("imageCtrl", function($scope, $http){
    
    $scope.getImages = function(){
        $http.get('/api/thumbnails',{params:{"url": $scope.url}}).then(function(response){
            $scope.images = response.data["thumbnails"];
            
            var i=0;
            var htm = "<p>Select A Thumbnail Below</p><br/>";
            var loc = document.getElementById("pics");
            
            for (i=0; i < $scope.images.length; i++){
                htm += "<img src="+ '"'+ $scope.images[i] +'"'+"onclick="+ '"giveThumbail(this)"'+"/>";
            }
            
            loc.innerHTML = htm;
        });
    };
});

app.controller("regCtrl", function($scope, $http){
    
    $scope.reg = function(){
        var fname = document.getElementById("first_name").value;
        var lname = document.getElementById("last_name").value;
        var uname = document.getElementById("username").value;
        var passw = document.getElementById("password").value;
        
        var data = {first_name: fname, last_name: lname, username: uname, password: passw};
    
        $http.post('/api/users/register', JSON.stringify(data)).then(function(res){
            if (res["status"] == 200){
                alert("200 OK");
            }
            else{
                alert("404 Not OK ");
            }
        });
    };
});

function giveThumbail(img){
        var loc = document.getElementById("thumbnail");
        loc.value = img.src;
}