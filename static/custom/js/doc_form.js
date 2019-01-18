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

function delete_row() {
    var table = document.getElementById('table_unit');  
    var inputs = table.getElementsByTagName("input");
    var i = inputs.length;
    while (i--) {
        var input = inputs[i];
        if (input.checked == true) {
            var tr = input.parentNode.parentNode;
            $(tr).attr("style", "display:none");
            //table.deleteRow(tr.rowIndex);
        }
    }
}

function checkboxes_sel_all(obj)
  {
  // Получаем NodeList дочерних элементов input формы:
  var items = obj.form.getElementsByTagName("input"), len, i;
 
  for (i = 0, len = items.length; i < len; i += 1)
    {
    // Если текущий элемент является чекбоксом
    if (items.item(i).type && items.item(i).type === "checkbox")
      {
      if (obj.checked)
        {
        // Устанавливаем отметки всем чекбоксам
        items.item(i).checked = true;
        }
      else
        {
        // Иначе снимаем отметки со всех чекбоксов:
        items.item(i).checked = false;
        }      
      }
    }
  }