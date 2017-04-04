// Your JavaScript Code here

var app = angular.module("imageApp", []);

app.controller("imageCtrl", function($scope, $http){
    $http.get('/api/thumbnails').then(function(response){
        $scope.images = response.data["thumbnails"];
    });
});