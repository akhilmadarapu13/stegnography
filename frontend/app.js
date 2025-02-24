var app = angular.module('stegoApp', []);

app.directive('fileModel', ['$parse', function($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('change', function() {
                $parse(attrs.fileModel).assign(scope, element[0].files[0]);
                scope.$apply();
            });
        }
    };
}]);

app.controller('MainController', ['$scope', '$http', function($scope, $http) {
    // Hide Text
    $scope.hideText = function() {
        var formData = new FormData();
        formData.append('image', $scope.imageFile);
        formData.append('message', $scope.inputText);
        formData.append('password', $scope.password);

        $http.post('http://127.0.0.1:5000/encrypt', formData, {
            headers: { 'Content-Type': undefined }
        }).then(function(response) {
            alert(response.data.message);
            $scope.stegoImageUrl = response.data.imagePath;
        }, function(error) {
            alert('Error: ' + error.data.error);
        });
    };

    // Extract Text
    $scope.extractText = function() {
        var formData = new FormData();
        formData.append('image', $scope.extractImageFile);
        formData.append('password', $scope.extractPassword);

        $http.post('http://127.0.0.1:5000/decrypt', formData, {
            headers: { 'Content-Type': undefined }
        }).then(function(response) {
            alert(response.data.message);
            $scope.extractedText = response.data.decodedMessage;
        }, function(error) {
            alert('Error: ' + error.data.error);
        });
    };
}]);
