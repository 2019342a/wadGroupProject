// +----------------------------------------------------------------+
// |  Controller for the story rooms of StoryTeller.                |
// +----------------------------------------------------------------+

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

  $scope.endSentence = "";


// ---------------------------------------------
//          Websockets setup and control
// ---------------------------------------------

  //Set up connections to routers when ready and get the story for the page.
  $dragon.onReady(function() {
    // Subscribe to the router for story updates
    $dragon.subscribe('story-router', $scope.channel, {id: $scope.storyId}).then(function(response) {
      $scope.dataMapper = new DataMapper(response.data);
    });

    // Subscribe to the router for control of the room
    $dragon.subscribe('room-control-router', $scope.controlChannel).then(function(response) {
      $dragon.callRouter('add_user', 'room-control-router', {user: $scope.user, storyid: $scope.storyId});
    });

    // Get the story for the current page
    $dragon.getSingle('story-router', {id:$scope.storyId}).then(function(response) {
      $scope.story = response.data;
      document.title = 'StoryTeller - ' + $scope.story.title;
      if ($scope.story.curr_user === "") {
        $dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
      }
    });

  });


  //Logic for messages on routers
  $dragon.onChannelMessage(function(channels,message) {
    // Story router
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

    // Room control router
    if (indexOf.call(channels, $scope.controlChannel) > -1) {
      if (message.comm === "update-time" ){
        $scope.timeLeft = 60;
      } else if (message.comm === "call-vote") {
        $scope.pause();
        $scope.voteToEnd(message.sentence);
      } else if (message.comm === "end") {
        $scope.storyEnd();
      } else if (message.comm === "resume") {
        $scope.resume();
      }
    }

  });


// ---------------------------------------------
//              Story writing logic
// ---------------------------------------------

  //Set timer
  var timer = setInterval(function() {
    $('#timer').text($scope.timeLeft--);
    if ($scope.timeLeft == $scope.stickTime - 1) {
      $scope.timeLeft = $scope.stickTime;
      if ($scope.isTurn && $scope.stickTime === 0) {
        $scope.clearAndGetNextUser();
      }
    }
  }, 1000);

  //Change window title when it is the current users turn and the window doesn't have focus
  $(window).blur(function() {
    if ($scope.story.curr_user === $scope.user){
      document.title =  "**StoryTeller - " + $scope.story.title;
    }
  });
  $(window).focus(function() {
    document.title = "StoryTeller - " + $scope.story.title;
  });

  // Submit sentence to story, call the router to add the sentence
  $scope.submit = function(story) {
    var newSentence =  $('#sentence-input-box').val();

    story.story_text = $scope.story.story_text + " " + $scope.fixSentenceGrammar(newSentence);
    $dragon.update('story-router', story);

    $scope.clearAndGetNextUser();
  }

  //Append a full stop if missing, and capitalise first letter
  $scope.fixSentenceGrammar = function(str) {
    str = str.charAt(0).toUpperCase() + str.substr(1);

    if (str.substr(str.length -1) != "."){
      return str + ".";
    } else {
      return str;
    }
  }

  //Clear the input box and call the router to get the next user
  $scope.clearAndGetNextUser = function() {
    document.getElementById('sentence-input-box').value='';
    $scope.isTurn = false;

    $dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
  }

  //Remove the user from the story if they close the window or leave the page

  $scope.removeUser = function() {
    $dragon.callRouter('remove_user', 'room-control-router', {user: username, storyid: extStoryId});
    if ($scope.story.curr_user === $scope.user) {
      $dragon.callRouter('next_user', 'room-control-router', {storyid: $scope.storyId, prev_user: $scope.user});
    }
  }

  window.onbeforeunload = $scope.removeUser;


// ---------------------------------------------
//                 Voting logic
// ---------------------------------------------

  // Call the vote to end the story
  $scope.callVote = function() {
    var newSentence = $('#sentence-input-box').val();
    $dragon.callRouter('call_vote', 'room-control-router', {sentence: newSentence, storyid:$scope.storyId});
  }

  // Pause the story progression during voting
  $scope.pause = function() {
    $('#sentence-input-box').attr('disabled', 'disabled');
    $('#endbutton').attr('disabled', 'disabled');
    $('#submitbutton').attr('disabled', 'disabled');
    $scope.stickTime = $scope.timeLeft;
  }

  // Show the voting panel once a vote has been called
  $scope.voteToEnd = function(sentence) {
    $scope.endSentence = $scope.fixSentenceGrammar(sentence);
    $("#endSentence").html($scope.endSentence);
    $("#endStoryModal").modal({
      backdrop: 'static',
      keyboard: false
    });
  }

  // Accept a vote to end the story
  $scope.voteEnd = function() {
    $dragon.callRouter('vote_end', 'room-control-router', {storyid:$scope.storyId, sentence:$scope.endSentence});
    $('#endStoryModal').modal('hide');
    $('#voteWaitingModal').modal({
      backdrop: 'static',
      keyboard: false
    });
  }

  //Accept a vote not to end the story
  $scope.voteDontEnd = function() {
    $dragon.callRouter('vote_dont_end', 'room-control-router', {storyid:$scope.storyId});
    $("#endStoryModal").modal('hide');
    $('#voteWaitingModal').modal({
      backdrop: 'static',
      keyboard: false
    });
  }

  // Resume the story in the event of a vote not to end the story
  $scope.resume = function() {
    $('#endStoryModal').modal('hide');
    $('#voteWaitingModal').modal('hide');
    $('#sentence-input-box').removeAttr('disabled');
    $('#endbutton').removeAttr('disabled');
    $('#submitbutton').removeAttr('disabled');
    $scope.stickTime = 0;
    if ($scope.story.curr_user === $scope.user) {
      $scope.clearAndGetNextUser();
    }
  }


// ---------------------------------------------
//              Story ending logic
// ---------------------------------------------

  // Unsubscribe users from the story channels and show a dialog to return them to the main page
  $scope.storyEnd = function() {
    $dragon.unsubscribe('room-control-router', $scope.controlChannel);
    $dragon.unsubscribe('story-router', $scope.channel);
    $('#endModal').modal({
      backdrop: 'static',
      keyboard: false
    });
  }

  // Return the user to the home page in the result of a story ending
  $scope.returnToHome = function() {
    location.reload();
  }

}]);
