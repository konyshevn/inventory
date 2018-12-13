function add_row() {
    //alert("HI");

    var tu= $('#table_unit'), tr= $('#table_unit tr:last');

    tr.find('.selectized').each(function(){
     $(this)[0].selectize.destroy();   
    })

    var cloned = tr.clone();  
    tr.find('.selectize_widget').each(function(){
        selectize_widget_init($(this))
    })

    cloned.find('.selectize_widget').each(function(){
        selectize_widget_init($(this))
    })

    //tr.find('selectize').removeAttr('data-select2-id').removeAttr('id').select2();
    //cloned.find('select').selectize()

    tu.append(cloned);
}  