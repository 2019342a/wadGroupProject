$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#myTab a[href="#top"]').tab('show')
$('#myTab a[href="#new"]').tab('show')
$('#myTab a[href="#popular"]').tab('show')

$('#likes').click(function(){
    var storyid;
    var like;
    storyid = $(this).attr("data-storyid");
    like = $(this).attr("data-like");
    $.get('/storyteller/rate_story/', {story_id: storyid, like: like}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
               $('#dislikes').hide();
    });
});

$('#dislikes').click(function(){
    var storyid;
    var like;
    storyid = $(this).attr("data-storyid");
    like = $(this).attr("data-like");
    $.get('/storyteller/rate_story/', {story_id: storyid, like: like}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
               $('#dislikes').hide();
    });
});