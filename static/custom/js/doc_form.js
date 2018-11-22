function add_row() {
    //alert("HI");

    var tu= $('#table_unit'), tr= $('#table_unit tr:last');

    tr.find('select').select2('destroy');

    var cloned = tr.clone();  

    tr.find('select').removeAttr('data-select2-id').removeAttr('id').select2();
    cloned.find('select').select2()

    tu.append(cloned);
}  