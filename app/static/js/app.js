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

function giveThumbail(img){
        var loc = document.getElementById("thumbnail");
        loc.value = img.src;
}