$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#myTab a[href="#top"]').tab('show')
$('#myTab a[href="#new"]').tab('show')
$('#myTab a[href="#popular"]').tab('show')

$('#likes').click(function(){
    var storyid;
    storyid = $(this).attr("data-storyid");
    console.log(storyid);
    $.get('/storyteller/rate_story/', {story_id: storyid}, function(data){
               $('#like_count').html(data);
               $('#likes').hide();
    });
});