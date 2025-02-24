var app = angular.module('stegoApp', []);

// Directive to bind file input to AngularJS scope
app.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function () {
                scope.$apply(function () {
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);

// Main Controller
app.controller('MainController', ['$scope', '$http', function ($scope, $http) {
    const baseUrl = 'http://127.0.0.1:5000';

    // Hide Text in Image
    $scope.hideText = function () {
        if (!$scope.imageFile || !$scope.inputText || !$scope.password) {
            alert('Please provide all inputs!');
            return;
        }

        var formData = new FormData();
        formData.append('image', $scope.imageFile);
        formData.append('message', $scope.inputText);
        formData.append('password', $scope.password);

        $http.post(baseUrl + '/encrypt', formData, {
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            $scope.stegoImageUrl = response.data.imagePath;
            alert('Image encrypted successfully! Download your image.');
        }, function (error) {
            alert('Error: ' + error.data.error);
        });
    };

    // Extract Text from Image
    $scope.extractText = function () {
        if (!$scope.extractImageFile || !$scope.extractPassword) {
            alert('Please provide both image and password!');
            return;
        }

        var formData = new FormData();
        formData.append('image', $scope.extractImageFile);
        formData.append('password', $scope.extractPassword);

        $http.post(baseUrl + '/decrypt', formData, {
            headers: { 'Content-Type': undefined }
        }).then(function (response) {
            $scope.extractedText = response.data.decodedMessage;
            alert('Decryption successful!');
        }, function (error) {
            alert('Error: ' + error.data.error);
        });
    };
}]);
