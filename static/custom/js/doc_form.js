function add_row() {
    //alert("HI");

    var tu= $('#table_unit'), tr= $('#table_unit tr:last');

    tr.find('.selectized').each(function(){
     $(this)[0].selectize.destroy();   
    })

    var cloned = tr.clone();  
    tr.find('.selectize_widget').each(function(){
        var field_id = $(this).data("field_id")
        $(this).selectize({
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
    })

    cloned.find('.selectize_widget').each(function(){
        var field_id = $(this).data("field_id")
        $(this).selectize({
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
    })

    //tr.find('selectize').removeAttr('data-select2-id').removeAttr('id').select2();
    //cloned.find('select').selectize()

    tu.append(cloned);
}  