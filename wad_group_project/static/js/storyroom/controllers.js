var RoomControllers = angular.module('RoomControllers', []);

RoomControllers.controller('StoryCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    
    $scope.story = {};
    
    $scope.channel = 'rooms';
    $scope.controlChannel = extStoryId + 'channel';

    $scope.storyId = extStoryId;
    $scope.user = username;
    $scope.category = category;
    
    $scope.timeLeft = 0;
    $scope.isTurn = false;

    
    $(window).blur(function() {
	if ($scope.story.curr_user === $scope.user){
	    document.title =  "**StoryTeller - " + $scope.story.title;
	}
    });

    $(window).focus(function() {
	document.title = "StoryTeller - " + $scope.story.title;
    });
		   
    
    function removeUser() {
	$dragon.callRouter('remove_user', 'room-control-router', {user: username, storyid: extStoryId});
	if ($scope.story.curr_user === $scope.user) {
	    $dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
	}
    }

    function fixSentenceGrammar(str) {
	str = str.charAt(0).toUpperCase() + str.substr(1);
	    
	if (str.substr(str.length -1) != "."){
	    return str + ".";
	} else {
	    return str;
	}
    }

    function clearAndGetNextUser() {
	document.getElementById('sentence-input-box').value='';
	$scope.isTurn = false;
	
	$dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});

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
	    if ($scope.story.curr_user === "") {
		$dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
	    }
	});

    });
    
    $dragon.onChannelMessage(function(channels,message) {
	if (indexOf.call(channels, $scope.channel) > -1) {
	    $scope.$apply(function() {
		$scope.dataMapper.mapData($scope.story, message);
	    });
	    
	    if ($scope.story.curr_user === $scope.user) {
		$('div#sentence-input').unblock();
		$scope.isTurn = true;
	    } else {
		$('div#sentence-input').block({ message: '<h4>Awaiting turn...</h4>'});
	    }

	}
	if (indexOf.call(channels, $scope.controlChannel) > -1) {
	    $scope.timeLeft = 60;
	}
	
    });

    $scope.submit = function(story) {
	var newSentence =  document.getElementById('sentence-input-box').value;
	
	story.story_text = $scope.story.story_text + " " + fixSentenceGrammar(newSentence); 
	$dragon.update('story-router', story);

	clearAndGetNextUser();
	
    }

   
    var timer = setInterval(function() {
	$('#timer').text($scope.timeLeft--);
	if ($scope.timeLeft == -1) {
	    $scope.timeLeft = 0;
	    if ($scope.isTurn) {
		clearAndGetNextUser();
	    }
	}
    }, 1000);
    
}]);			
