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

export function docmove() {
  this.id = null
  this.doc_date = (new Date).toISOString()
  this.doc_num = null
  this.active = false
  this.department_from = null
  this.department_to = null
  this.stock_from = null
  this.stock_to = null
  this.table_unit = [
    {
      id: /*null*/ `null_f${(+new Date).toString(16)}`,
      device: null,
      person_from: null,
      person_to: null,
      qty: '1',
      comment: '',
      DELETE: false,
    },
  ]
  this.comment = ''
} 

export function docinventory() {
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
      person_fact: null,
      person_accountg: null,
      qty_accountg: '1',
      qty_fact: '1',
      stock_fact: null,
      comment: '',
      DELETE: false,
    },
  ]
  this.comment = ''
} 