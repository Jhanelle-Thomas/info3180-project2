// Your JavaScript Code here
var app = angular.module("wishListApp", []);

app.controller("imageCtrl", function($scope, $http){
    
    $scope.getImages = function(){
        $http.get('/api/thumbnails',{params:{"url": $scope.url},
        'headers': {'Authorization': 'Bearer ' + localStorage.getItem('token')}
        }).then(function(response){
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

app.controller("thumbCtrl", function($scope, $http){
    
    var i = 0;
    var htm = "";
    var uid = document.getElementById("uid").value;
    var div = document.getElementById("wishes");
    
    $scope.delwish = function(itemid){
    
        $http.delete("/api/users/"+uid+"/wishlist/"+itemid, {
            'headers': {'Authorization': 'Bearer ' + localStorage.getItem('token')}
        }).then(function(res){
            if (res["status"] == 200){
                window.location = '/';
            }
            else{
                alert("404 Not OK ");
            }
        });
    };
    
    $http.get('/api/users/'+uid+'/wishlist', {
        'headers': {'Authorization': 'Bearer ' + localStorage.getItem('token')}
    }).then(function(res){
        
        for(i=0; i < res.data.length; i++){
            htm += "<hr/>";
            htm += "<p><b>Title: </b>"+res.data[i]["title"]+"</p><br/>";
            htm += "<img src="+'"'+res.data[i]["thumbnail"]+'"'+"/>";
            htm += "<p><b>Description: </b>"+res.data[i]["description"]+"</p><br/>";
            htm += "<p><b>Website URL: </b><a href ='"+res.data[i]["website"]+"'>"+ res.data[i]["website"] + "</a></p><br/>";
            htm += '<button type="submit" name="submit" class="btn btn-primary btn-block" onclick="calldelwish('+res.data[i]["itemid"]+')">Remove Wish Item</button>';
            htm += "<hr/>";
        }
        
        div.innerHTML = htm;
    });
});

app.controller("addCtrl", function($scope, $http){
    
    $scope.addWish = function(uid){
        var titl = document.getElementById("title").value;
        var desc = document.getElementById("description").value;
        var webs = document.getElementById("website").value;
        var thum = document.getElementById("thumbnail").value;
        
        var data = {title: titl, description: desc, website: webs, thumbnail: thum};
        
        $http.post('/api/users/'+uid+'/wishlist', JSON.stringify(data), {
        'headers': {'Authorization': 'Bearer ' + localStorage.getItem('token')}
        }).then(function(res){
            if (res["status"] == 200){
                window.location = '/';
                alert("Your item was successfully added to your wishlist")
            }
            else{
                alert("There was an error, your item was not added to your wishlist");
            }
        });
    };
});

app.controller("loginCtrl", function($scope, $http){
    $scope.token = '';
    $scope.login = function(){
        var uname = document.getElementById("username").value;
        var passw = document.getElementById("password").value;
        
        var data = {username: uname, password: passw};
        
        $http.post('/api/users/login', JSON.stringify(data)).then(function(response){
            if (response["status"] == 200){
                let token = response.data.data.token;
                localStorage.setItem('token', token);
                $scope.token = token;
                window.location = '/';
            }
            else{
                alert("404 Not OK ");
            }
        });
    }
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
                window.location = '/login';
            }
            else{
                alert("404 Not OK ");
            }
        });
    };
});

app.controller("shareCtrl", function($scope, $http){
    $scope.getemail = function(){
        var email = document.getElementById("email");
        
        if(email.style.display == "none"){
            email.style.display = "block";
        }
        else{
            email.style.display = "none";
        }
        
    };
    
    $scope.sendemail = function(){
        var uid = document.getElementById("uid").value;
        var name = document.getElementById("name").value;
        var email = document.getElementById("em").value;
        
        var data = {uid: uid, name: name, email: email};
        
        $http.post('/send', JSON.stringify(data), {
        'headers': {'Authorization': 'Bearer ' + localStorage.getItem('token')}
        }).then(function(res){
            if (res["status"] == 200){
                alert("Your wishlist was shared")
            }
            else{
                alert("There was an error, your wishlist was not shared");
            }
        });
        
    };
});

function giveThumbail(img){
        var loc = document.getElementById("thumbnail");
        loc.value = img.src;
}

function calldelwish(tid){
    var scope = angular.element(document.getElementById("wishes")).scope();
    scope.$apply(function () {
    scope.delwish(tid);
    });
}