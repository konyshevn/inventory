module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
    ? '/static/'
    : '/'
    /*
  ,css: {
    loaderOptions: {
      less:{

        // http://lesscss.org/usage/#less-options-strict-units `Global Variables`
        // `primary` — имя поля глобальных переменных
        globalVars: {
          "strictMath": true
        }
      }
    }
  }
  */
}