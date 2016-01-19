public class {{entity_name}}{
   {% for member in members %}
       private {{member.type}} {{member.name}};
   {% endfor %}
}