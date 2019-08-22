export function docincome() {
  this.id = null
  this.doc_date = '01'
  this.doc_num = ''
  this.active = false
  this.department = ''
  this.stock = ''
  this.table_unit = [
    {
      id: /*null*/ `null_f${(+new Date).toString(16)}`,
      device: '',
      person: '',
      qty: '1',
      comment: '',
      DELETE: false,
    },
  ]
  this.comment = ''

} 