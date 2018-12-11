$(document).ready(function() {
$('#id_department').selectize({
    create: false,
})

$('#myselectize').selectize({
      create: false,
      sortField: 'text',
      valueField: 'value',
      labelField: 'text',
      searchField: ['text'],
      openOnFocus: true,
    //  closeAfterSelect: true,

      render: {
        option: function (item, escape) {
            return '<div>' + escape(item.text) + '</div>';
        }
        },

      load: function(query, callback) {
        if (!query.length) return callback();
        //url = $("#myselectize").data('url');
        $.ajax({
          url: '/ajax/department/',
          data: { q: query},
          dataType: "json",
          type: 'GET',
          error: function() {
            console.log(res);
            callback();
          },
          success: function(res) {
            console.log(res);
            callback(res);
          }
        })
      },
      


});

})