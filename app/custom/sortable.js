import "sortable"; // imports from `sortable.min.js`

// Alternatively, you can use below to get JS module at runtime
// import 'https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.15.6/Sortable.min.js'
// and remove as dependency in sortable.py file

export default {
    template: `
    <div>
      <slot></slot>
    </div>
  `,
    props: {
        group: String,
    },
    mounted() {
        if (this.group === 'None') {
            this.group = this.$el.id;
        }
        this.sortableInstance = Sortable.create(this.$el, {
            group: this.group,
            animation: 150,
            // Using a handle would more secure as only elements with the class drop_handle can be moved.
            // handle: ".drop_handle",
            ghostClass: 'opacity-50',
            onEnd: (evt) => this.$emit("item-drop", {
                new_index: evt.newIndex,
                old_index: evt.oldIndex,
                new_list: parseInt(evt.to.id.slice(1)),
                old_list: parseInt(evt.from.id.slice(1)),
            }),
        });
    },
    methods: {
        setDisabled(value) {
            if (typeof value === "undefined"){
                value = this.sortableInstance.options.disabled;
                this.sortableInstance.option('disabled', !value);
            } else {
                this.sortableInstance.option('disabled', value);
            }
        },

    },
};
