// import moment from 'moment';

export function docincome() {
  this.id = null
  this.doc_date = (new Date).toISOString()
  this.doc_num = null
  this.active = false
  this.department = null
  this.stock = null
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

export function docwriteoff() {
  this.id = null
  this.doc_date = (new Date).toISOString()
  this.doc_num = null
  this.active = false
  this.department = null
  this.stock = null
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