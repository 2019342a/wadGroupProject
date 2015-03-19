$('#myTab a').click(function (e) {
  e.preventDefault()
  $(this).tab('show')
})

$('#myTab a[href="#top"]').tab('show')
$('#myTab a[href="#new"]').tab('show')
$('#myTab a[href="#popular"]').tab('show')
