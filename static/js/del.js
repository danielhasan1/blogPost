function deleteentry(entry){
	//$(entry).parent().remove()
	var $entry = $(entry)
	$entry.parent().remove()
	var id = $entry.data('id')
	console.log(id)
	$.ajax({
		url: 'comment/'+id+'/delete/',
	})
}