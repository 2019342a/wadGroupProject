var RoomControllers = angular.module('RoomControllers', []);

swampdragon.close(function() {
    swampdragon.callRouter('remove_user', 'room-control-router', {user: username, storyid: extStoryId});
});

RoomControllers.controller('StoryCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    $scope.story = {};
    $scope.channel = 'rooms';
    $scope.controlChannel = extStoryId + 'channel';
    $scope.timeLeft = 60;
    $scope.storyId = extStoryId;
    $scope.user = username;
    
    function removeUser() {
	$dragon.callRouter('remove_user', 'room-control-router', {user: username, storyid: extStoryId});
	if ($scope.story.curr_user === $scope.user) {
	    $dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
	}
    }

    window.onbeforeunload = removeUser;

    $dragon.onReady(function() {
	$dragon.subscribe('story-router', $scope.channel, {id: $scope.storyId}).then(function(response) {
	    $scope.dataMapper = new DataMapper(response.data);
	});

	$dragon.subscribe('room-control-router', $scope.controlChannel).then(function(response) {
	    $dragon.callRouter('add_user', 'room-control-router', {user: $scope.user, storyid: $scope.storyId});
	});
	
	$dragon.getSingle('story-router', {id:$scope.storyId}).then(function(response) {
	    $scope.story = response.data;
	    document.title = 'StoryTeller - ' + $scope.story.title;
	});

    });
    
    $dragon.onChannelMessage(function(channels,message) {
	if (indexOf.call(channels, $scope.channel) > -1) {
	    $scope.$apply(function() {
		$scope.dataMapper.mapData($scope.story, message);
	    });
	    
	    if ($scope.story.curr_user === $scope.user) {
		$('div#sentence-input').unblock();
	    } else {
		$('div#sentence-input').block({ message: '<h4>Awaiting turn...</h4>'});
	    }
	    $scope.timeLeft = 60;
	}
    });

    $scope.submit = function(story) {
	function capitalizeFirstLetter(string) {
	    return string.charAt(0).toUpperCase() + string.slice(1);
	}
	
	var newSentence =  document.getElementById('sentence-input-box').value;
	if (newSentence.substr(newSentence.length -1) != "."){
	    var end = ".";
	} else {
	    var end = "";
	}
	story.story_text = $scope.story.story_text + " " + capitalizeFirstLetter(newSentence) + end; 

	$dragon.update('story-router', story);
	
	document.getElementById('sentence-input-box').value='';
	
	$dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
    }

   
    var timer = setInterval(function() {
	$('#timer').text($scope.timeLeft--);
	if ($scope.timeLeft == -1) {
	    if ($scope.isTurn) {
		//$('div#sentence-input').block({ message: '<h4>Awaiting turn...</h4>'});
		$dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
	    }
	    $scope.timeLeft = 60;
	}
    }, 1000);
    
}]);			
