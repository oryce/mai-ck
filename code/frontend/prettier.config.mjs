/**
 * @see https://prettier.io/docs/configuration
 * @type {import("prettier").Config}
 */
const config = {
  tabWidth: 2,
  trailingComma: 'es5',
  semi: false,
  singleQuote: true,

  plugins: ['prettier-plugin-tailwindcss'],

  tailwindStylesheet: './src/app/globals.css',
  tailwindFunctions: ['clsx'],
}

export default config
