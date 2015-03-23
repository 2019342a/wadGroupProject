var RoomControllers = angular.module('RoomControllers', []);

RoomControllers.controller('StoryCtrl', ['$scope', '$dragon', function($scope, $dragon) {
    
    $scope.story = {};
    
    $scope.channel = 'rooms';
    $scope.controlChannel = extStoryId + 'channel';

    $scope.storyId = extStoryId;
    $scope.user = username;
    $scope.category = category;

    $scope.stickTime = 0;
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

    var timer = setInterval(function() {
	$('#timer').text($scope.timeLeft--);
	if ($scope.timeLeft == $scope.stickTime - 1) {
	    $scope.timeLeft = $scope.stickTime;
	    if ($scope.isTurn && $scope.stickTime === 0) {
		clearAndGetNextUser();
	    }
	}
    }, 1000);
		   
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
		$scope.isTurn = true;
		$('div#sentence-input').unblock();
		$('#sentence-input-box').removeAttr('disabled');
		$('#endbutton').removeAttr('disabled');
		$('#submitbutton').removeAttr('disabled');
	    } else {
		$('div#sentence-input').block({ message: '<h4>Awaiting turn...</h4>'});
		$('#sentence-input-box').attr('disabled', 'disabled');
		$('#endbutton').attr('disabled', 'disabled');
		$('#submitbutton').attr('disabled', 'disabled');
	    }

	}
	if (indexOf.call(channels, $scope.controlChannel) > -1) {
	    if (message.comm === "update-time" ){
		$scope.timeLeft = 60;
	    } else if (message.comm === "call-vote") {
		$scope.pause();
		$scope.end(message.sentence);
	    } else if (message.comm === "end") {
		$scope.storyEnd();
	    } else if (message.comm === "resume") {
		$scope.resume();
	    }
	}
	
    });

    $scope.submit = function(story) {
	var newSentence =  document.getElementById('sentence-input-box').value;
	
	story.story_text = $scope.story.story_text + " " + fixSentenceGrammar(newSentence); 
	$dragon.update('story-router', story);

	clearAndGetNextUser();
	
    }

    $scope.callVote = function() {
	var newSentence =  document.getElementById('sentence-input-box').value;
	$dragon.callRouter('call_vote', 'room-control-router', {sentence: newSentence, storyid:$scope.storyId});
    }
    
    $scope.voteEnd = function() {
	$dragon.callRouter('vote_end', 'room-control-router', {storyid:$scope.storyId});
	$('#endStoryModal').modal('hide');
	$('#voteWaitingModal').modal({
	    backdrop: 'static',
	    keyboard: false
	});
    }

    $scope.voteDontEnd = function() {
	$("#endStoryModal").modal('hide');
	$('#voteWaitingModal').modal({
	    backdrop: 'static',
	    keyboard: false
	});
    }

    $scope.end = function(sentence) {
	$scope.voteTimeLeft = 20;
	var voteTimer = setInterval(function() {
	    if ($scope.voteTimeLeft == -1 && $scope.story.ended === false) {
		$scope.notEnd();
	    }
	}, 1000);
	$("#endSentence").html(fixSentenceGrammar(sentence));
	$("#endStoryModal").modal({
	    backdrop: 'static',
	    keyboard: false
	});
    }

    $scope.storyEnd = function() {
	$('#endModal').modal({
	    backdrop: 'static',
	    keyboard: false
	});
    }

    $scope.pause = function() {
	$('#sentence-input-box').attr('disabled', 'disabled');
	$('#endbutton').attr('disabled', 'disabled');
	$('#submitbutton').attr('disabled', 'disabled');
	$scope.stickTime = $scope.timeLeft;
    }

    $scope.resume = function() {
	$('#endStoryModal').modal('hide');
	$('#voteWaitingModal').modal('hide');
	$('#sentence-input-box').removeAttr('disabled');
	$('#endbutton').removeAttr('disabled');
	$('#submitbutton').removeAttr('disabled');
	$scope.stickTime = 0;
    }

    $scope.notEnd = function() {
	$dragon.callRouter('not_ending', 'room-control-router', {storyid:$scope.storyId})
    }

    $scope.returnToHome = function() {
	location.reload();
    }
    
}]);			
