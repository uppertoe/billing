document.querySelectorAll('.select').forEach((el) => {
  let settings = {};
  new TomSelect(el, settings);
  el.parentElement.lastElementChild.classList.remove('form-select');
});

document.querySelectorAll('.selectmultiple').forEach((el) => {
  let settings = {
    plugins: {
      remove_button: {
        title: 'Remove this item',
      },
    },
    duplicates: true,
    hideSelected: false,
    placeholder: 'Type to search',
    hidePlaceholder: true,
  };
  new TomSelect(el, settings);
  el.parentElement.lastElementChild.classList.remove('form-select');
});
