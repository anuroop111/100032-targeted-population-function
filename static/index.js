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
            start_point:$("input[name='start_point_date']").val(),
            end_point: $("input[name='end_point_date']").val(),
            split:$("select[name='split']").val(),
        }
        const number_of_variable = Number($("input[name='number_of_variable']").val());

        const distribution_input={
            normal:Number($("input[name='normal']").val()),
            poisson:Number($("input[name='poisson']").val()),
            binomial:Number($("input[name='binomial']").val()),
            bernoulli:Number($("input[name='bernoulli']").val()),
        }

        const bernoulli = {
            error_size: Number($("input[name='error_size']").val()),
            test_number: Number($("input[name='test_number']").val()),
            selection_start_point: Number($("input[name='selection_start_point']").val()),
            items_to_be_selected: Number($("input[name='items_to_be_selected']").val()),
        }

        const binomial = {
            split_choice: $("select[name='split_choice']").val(),
            marginal_error: Number($("input[name='marginal_error']").val()),
            split_decision: $("select[name='split_decision']").val(),
            error: Number($("input[name='error']").val()),
            function: $("select[name='function']").val(),
            user_choice_field: $("input[name='user_choice_field']").val(),
            user_choice_value: $("input[name='user_choice_value']").val(),
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

        console.log(start_point);


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
            bernoulli:bernoulli,
            binomial:binomial
        }
        console.log(request_data)
        $("#output-section").html("<h2>loading....</h2>");


        $.ajax({
                url: "/api/targeted_population/",
                type: 'post',
                contentType: "application/json; charset=utf-8",
                data:  JSON.stringify(request_data),
                success: function(data) {

                  $("#output-section").html(data);
                },

                error: function (request, status, error) {

                    $("#output-section").html(error);

                }
        });

    });
});
