function selectize_widget_init(item) {
    var field_id = item.data("field_id")
    //console.log(field_id);
    var $select = item.selectize({
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
                url: '/selectize_ajax_query/',
                data: { 'q': query, 'field_id': field_id },
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
    $select[0].selectize.on( 'dropdown_close', function () {
        $select[0].selectize.clearOptions();
    });
}

$(document).ready(function() {

    $('.selectize_widget').each(function(index) {
        selectize_widget_init($(this))
    })
})