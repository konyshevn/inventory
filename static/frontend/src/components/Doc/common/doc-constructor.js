export function docincome() {
  this.id = null
  this.doc_date = new Date
  this.doc_num = null
  this.active = false
  this.department = ''
  this.stock = ''
  this.table_unit = [
    {
      id: /*null*/ `null_f${(+new Date).toString(16)}`,
      device: null,
      person: null,
      qty: '1',
      comment: '',
      DELETE: false,
    },
  ]
  this.comment = ''

} 