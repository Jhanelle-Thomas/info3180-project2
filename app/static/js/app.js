// Your JavaScript Code here
var app = angular.module("wishListApp", []);

app.controller("imageCtrl", function($scope, $http){
    
    $scope.getImages = function(){
        $http.get('/api/thumbnails',{params:{"url": $scope.url}}).then(function(response){
            $scope.images = response.data["thumbnails"];
            
            var i=0;
            var htm = "";
            var loc = document.getElementById("pics");
            
            for (i=0; i < $scope.images.length; i++){
                htm += "<img src="+ '"'+ $scope.images[i] +'"' +"/>";
            }
            
            loc.innerHTML = htm;
        });
    };
});