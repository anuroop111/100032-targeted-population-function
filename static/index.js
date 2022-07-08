console.log("js loaded");

$(document).ready(function (event) {

    $("#targeted-population-form").submit(function(e) {
        e.preventDefault();
        const fields = $("input[name='fields']").val().split(",");

        const database_details={
            database:$("input[name='database']").val() ,
            collection:$("input[name='collection']").val(),
            fields: fields,
        }



        const time_input={
            period:$("select[name='period']").val(),
            start_point:$("input[name='start_point']").val(),
            end_point: $("input[name='end_point']").val(),
            split:$("input[name='split']").val(),
        }
        const number_of_variable = Number($("input[name='number_of_variable']").val());

        const distribution_input={
            normal:Number($("input[name='normal']").val()),
            poisson:Number($("input[name='poisson']").val()),
            binomial:Number($("input[name='binomial']").val()),
            bernoulli:Number($("input[name='bernoulli']").val()),
        }

        const data_types=[];
        $('input[name="datatype"]').each(function(){
            data_types.push( $(this).val());
        });

        const m_or_A_selction=[];
        $('select[name="m_or_A_selction"]').each(function(){
            m_or_A_selction.push( $(this).val());
        });

        const m_or_A_value=[];
        $('input[name="m_or_A_value"]').each(function(){
            m_or_A_value.push( $(this).val());
        });

        const error=[];
        $('input[name="error"]').each(function(){
            error.push( $(this).val());
        });

        const r=[];
        $('input[name="r"]').each(function(){
            r.push( $(this).val());
        });

        const start_point=[];
        $('input[name="start_point"]').each(function(){
            start_point.push( $(this).val());
        });

        const end_point=[];
        $('input[name="end_point"]').each(function(){
            end_point.push( $(this).val());
        });


        const a=[];
        $('input[name="a"]').each(function(){
            a.push( $(this).val());
        });

        const stage_input_list=[];
        for(let index=0; index<data_types.length; index++){
            if(data_types[index] !=""){

                if(data_types[index]=="7"){
                    const stage ={
                        'data_type': 7,
                        'p_r_selection':$("select[name='p_r_selection']").val(),
                        'proportion':Number($("input[name='proportion']").val()),
                        'first_position':Number($("input[name='first_position']").val()),
                        'last_position':Number($("input[name='last_position']").val()),
                    }

                    stage_input_list.push(stage);
                    continue;

                }

                  const stage = {
                    'data_type':Number(data_types[index]),
                    'm_or_A_selction': m_or_A_selction[index],
                    'm_or_A_value': Number(m_or_A_value[index]),
                    'error': Number(error[index]),
                    'r': Number(r[index]),
                    'start_point': start_point[index],
                    'end_point': end_point[index],
                    'a': Number(a[index]),
                }

                stage_input_list.push(stage)

            }
        }

        const request_data ={
             database_details: database_details,
            distribution_input: distribution_input,
            number_of_variable:number_of_variable,
            stages:stage_input_list,
            time_input:time_input,
        }
        console.log(request_data)
        $("#output-section").html("<h2>loading....</h2>");


        $.ajax({
                url: "/api/targeted_population/",
                type: 'post',
                contentType: "application/json; charset=utf-8",
                data:  JSON.stringify(request_data),
                success: function(data) {
                  if(data["normal"]['is_error']==true){
                     $("#output-section").html(data["normal"]["error_text"]);
                  }

                  else{
                      let output_html = ""

                      for(let i=0; i<data["normal"]["data"].length; i++){

                         output_html = output_html + "<h2>" + fields[i] + "</h2>"

                        for(row in data[i]){
                            output_html = output_html + "<div class='row'><div class='col-3'>" + row['eventId'] +"</div>" + "<div class='col-3'>" + row[fields[i]] +"</div></div>";
                        }
                      }

                      $("#output-section").html(output_html);

                       $("#output-section-poisson").html(data["poisson"]);
                       $("#output-section-binomial").html(data["binomial"]);
                        $("#output-section-bern").html(data["bernoulli"]);

                  }
                },

                error: function (request, status, error) {

                    $("#output-section").html(error);

                }
        });

    });
});
