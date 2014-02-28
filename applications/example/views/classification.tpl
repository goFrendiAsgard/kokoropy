<style type="text/css">
    textarea{
        font-size: x-small!important;
        font-family: 'courier';
    }
</style>
<div class="alert alert-info">
    <ul>
        <li>
            You should provide training and testing data in csv format. If you don't have any idea about it, you can just simply use
            <a id="btn_partial_iris" class="btn btn-success" href="#">partial iris dataset</a> or <a id="btn_complete_iris" class="btn btn-success" href="#">complete iris dataset</a> and see how it works.<br />
            For more information about iris dataset, please visit <a target="blank" href="http://archive.ics.uci.edu/ml/datasets/Iris">http://archive.ics.uci.edu/ml/datasets/Iris</a>
        </li>
        <li>
            To fill out the parameters, please refer <a target="blank" href="http://scikit-learn.org/0.13/modules/classes.html">http://scikit-learn.org/0.13/modules/classes.html</a>
        </li>
        <li>
            We use scikit-learn 0.1.4, if you use older version or don't have scikit-learn installed in your server, please do <i>sudo pip install -U scikit-learn</i>
        </li>
    </ul>
</div>
<h3>Data Classification Example</h3>
<form action="{{ BASE_URL }}example/classification_result" method="post" enctype="multipart/form-data" id="classification-form" class="form-horizontal" role="form">
    <div class="form-group">
        <label for="draw_plot" class="col-lg-3 col-md-3 control-label">Draw Data Plot</label>
        <div class="col-lg-7 col-md-8">
            <input type="checkbox" id="draw_plot" name="draw_plot" value="true" checked>
        </div>
    </div>
    <div class="form-group">
        <label for="training_csv" class="col-lg-3 col-md-3 control-label">CSV Training Data</label>
        <div class="col-lg-7 col-md-8">
            <textarea class="form-control" id="training_csv" name="training_csv" placeholder="Training Data in csv format (with captions)."></textarea>
            <p class="help-block">
                Put your training data in csv format (1st row should be caption)
            </p>
        </div>
    </div>
    <div class="form-group">
        <label for="testing_csv" class="col-lg-3 col-md-3 control-label">CSV Testing Data</label>
        <div class="col-lg-7 col-md-8">
            <textarea class="form-control" id="testing_csv" name="testing_csv" placeholder="Testing Data in csv format (without captions)"></textarea>
            <p class="help-block">
                Put your testing data in csv format (no caption)
            </p>
        </div>
    </div>
    <div class="form-group">
        <label for="predict_csv" class="col-lg-3 col-md-3 control-label">CSV Data to Predict</label>
        <div class="col-lg-7 col-md-8">
            <textarea class="form-control" id="predict_csv" name="predict_csv" placeholder="Data to Predict in csv format (without captions)"></textarea>
            <p class="help-block">
                Put your prediction data in csv format
            </p>
        </div>
    </div>
    <div class="form-group">
        <label for="classifier" class="col-lg-3 col-md-3 control-label">Classifier</label>
        <div class="col-lg-7 col-md-8">
            <select class="form-control" id="classifier" name="classifier" placeholder="Target Caption">
                % for classifier in classifiers:
                    <option value="{{ classifier }}">{{ classifier }}</option>
                % end
            </select>
        </div>
    </div>
    <div id="parameters">&nbsp;</div>
    <div class="form-group">
        <div class="col-lg-offset-3 col-md-offset-3 col-lg-7 col-md-8">
            <input class="btn btn-primary" name="btn_classify" value="Do classification" type="submit" />
            <input name="action" value="add" type="hidden" />
        </div>
    </div>
</form>
<div id="result">Here will be the result</div>
<script type="text/javascript" src="{{ BASE_URL }}index/assets/static_libraries/autosize/jquery.autosize.min.js"></script>
% import json
<script type="text/javascript">
    var CLASSIFIERS = {{ !json.dumps(classifiers) }};
    var COMPLETE_IRIS_CSV = 'sepal length, sepal width, petal length, petal width, class\n5.1,3.5,1.4,0.2,Iris-setosa\n4.9,3.0,1.4,0.2,Iris-setosa\n4.7,3.2,1.3,0.2,Iris-setosa\n4.6,3.1,1.5,0.2,Iris-setosa\n5.0,3.6,1.4,0.2,Iris-setosa\n5.4,3.9,1.7,0.4,Iris-setosa\n4.6,3.4,1.4,0.3,Iris-setosa\n5.0,3.4,1.5,0.2,Iris-setosa\n4.4,2.9,1.4,0.2,Iris-setosa\n4.9,3.1,1.5,0.1,Iris-setosa\n5.4,3.7,1.5,0.2,Iris-setosa\n4.8,3.4,1.6,0.2,Iris-setosa\n4.8,3.0,1.4,0.1,Iris-setosa\n4.3,3.0,1.1,0.1,Iris-setosa\n5.8,4.0,1.2,0.2,Iris-setosa\n5.7,4.4,1.5,0.4,Iris-setosa\n5.4,3.9,1.3,0.4,Iris-setosa\n5.1,3.5,1.4,0.3,Iris-setosa\n5.7,3.8,1.7,0.3,Iris-setosa\n5.1,3.8,1.5,0.3,Iris-setosa\n5.4,3.4,1.7,0.2,Iris-setosa\n5.1,3.7,1.5,0.4,Iris-setosa\n4.6,3.6,1.0,0.2,Iris-setosa\n5.1,3.3,1.7,0.5,Iris-setosa\n4.8,3.4,1.9,0.2,Iris-setosa\n5.0,3.0,1.6,0.2,Iris-setosa\n5.0,3.4,1.6,0.4,Iris-setosa\n5.2,3.5,1.5,0.2,Iris-setosa\n5.2,3.4,1.4,0.2,Iris-setosa\n4.7,3.2,1.6,0.2,Iris-setosa\n4.8,3.1,1.6,0.2,Iris-setosa\n5.4,3.4,1.5,0.4,Iris-setosa\n5.2,4.1,1.5,0.1,Iris-setosa\n5.5,4.2,1.4,0.2,Iris-setosa\n4.9,3.1,1.5,0.1,Iris-setosa\n5.0,3.2,1.2,0.2,Iris-setosa\n5.5,3.5,1.3,0.2,Iris-setosa\n4.9,3.1,1.5,0.1,Iris-setosa\n4.4,3.0,1.3,0.2,Iris-setosa\n5.1,3.4,1.5,0.2,Iris-setosa\n5.0,3.5,1.3,0.3,Iris-setosa\n4.5,2.3,1.3,0.3,Iris-setosa\n4.4,3.2,1.3,0.2,Iris-setosa\n5.0,3.5,1.6,0.6,Iris-setosa\n5.1,3.8,1.9,0.4,Iris-setosa\n4.8,3.0,1.4,0.3,Iris-setosa\n5.1,3.8,1.6,0.2,Iris-setosa\n4.6,3.2,1.4,0.2,Iris-setosa\n5.3,3.7,1.5,0.2,Iris-setosa\n5.0,3.3,1.4,0.2,Iris-setosa\n7.0,3.2,4.7,1.4,Iris-versicolor\n6.4,3.2,4.5,1.5,Iris-versicolor\n6.9,3.1,4.9,1.5,Iris-versicolor\n5.5,2.3,4.0,1.3,Iris-versicolor\n6.5,2.8,4.6,1.5,Iris-versicolor\n5.7,2.8,4.5,1.3,Iris-versicolor\n6.3,3.3,4.7,1.6,Iris-versicolor\n4.9,2.4,3.3,1.0,Iris-versicolor\n6.6,2.9,4.6,1.3,Iris-versicolor\n5.2,2.7,3.9,1.4,Iris-versicolor\n5.0,2.0,3.5,1.0,Iris-versicolor\n5.9,3.0,4.2,1.5,Iris-versicolor\n6.0,2.2,4.0,1.0,Iris-versicolor\n6.1,2.9,4.7,1.4,Iris-versicolor\n5.6,2.9,3.6,1.3,Iris-versicolor\n6.7,3.1,4.4,1.4,Iris-versicolor\n5.6,3.0,4.5,1.5,Iris-versicolor\n5.8,2.7,4.1,1.0,Iris-versicolor\n6.2,2.2,4.5,1.5,Iris-versicolor\n5.6,2.5,3.9,1.1,Iris-versicolor\n5.9,3.2,4.8,1.8,Iris-versicolor\n6.1,2.8,4.0,1.3,Iris-versicolor\n6.3,2.5,4.9,1.5,Iris-versicolor\n6.1,2.8,4.7,1.2,Iris-versicolor\n6.4,2.9,4.3,1.3,Iris-versicolor\n6.6,3.0,4.4,1.4,Iris-versicolor\n6.8,2.8,4.8,1.4,Iris-versicolor\n6.7,3.0,5.0,1.7,Iris-versicolor\n6.0,2.9,4.5,1.5,Iris-versicolor\n5.7,2.6,3.5,1.0,Iris-versicolor\n5.5,2.4,3.8,1.1,Iris-versicolor\n5.5,2.4,3.7,1.0,Iris-versicolor\n5.8,2.7,3.9,1.2,Iris-versicolor\n6.0,2.7,5.1,1.6,Iris-versicolor\n5.4,3.0,4.5,1.5,Iris-versicolor\n6.0,3.4,4.5,1.6,Iris-versicolor\n6.7,3.1,4.7,1.5,Iris-versicolor\n6.3,2.3,4.4,1.3,Iris-versicolor\n5.6,3.0,4.1,1.3,Iris-versicolor\n5.5,2.5,4.0,1.3,Iris-versicolor\n5.5,2.6,4.4,1.2,Iris-versicolor\n6.1,3.0,4.6,1.4,Iris-versicolor\n5.8,2.6,4.0,1.2,Iris-versicolor\n5.0,2.3,3.3,1.0,Iris-versicolor\n5.6,2.7,4.2,1.3,Iris-versicolor\n5.7,3.0,4.2,1.2,Iris-versicolor\n5.7,2.9,4.2,1.3,Iris-versicolor\n6.2,2.9,4.3,1.3,Iris-versicolor\n5.1,2.5,3.0,1.1,Iris-versicolor\n5.7,2.8,4.1,1.3,Iris-versicolor\n6.3,3.3,6.0,2.5,Iris-virginica\n5.8,2.7,5.1,1.9,Iris-virginica\n7.1,3.0,5.9,2.1,Iris-virginica\n6.3,2.9,5.6,1.8,Iris-virginica\n6.5,3.0,5.8,2.2,Iris-virginica\n7.6,3.0,6.6,2.1,Iris-virginica\n4.9,2.5,4.5,1.7,Iris-virginica\n7.3,2.9,6.3,1.8,Iris-virginica\n6.7,2.5,5.8,1.8,Iris-virginica\n7.2,3.6,6.1,2.5,Iris-virginica\n6.5,3.2,5.1,2.0,Iris-virginica\n6.4,2.7,5.3,1.9,Iris-virginica\n6.8,3.0,5.5,2.1,Iris-virginica\n5.7,2.5,5.0,2.0,Iris-virginica\n5.8,2.8,5.1,2.4,Iris-virginica\n6.4,3.2,5.3,2.3,Iris-virginica\n6.5,3.0,5.5,1.8,Iris-virginica\n7.7,3.8,6.7,2.2,Iris-virginica\n7.7,2.6,6.9,2.3,Iris-virginica\n6.0,2.2,5.0,1.5,Iris-virginica\n6.9,3.2,5.7,2.3,Iris-virginica\n5.6,2.8,4.9,2.0,Iris-virginica\n7.7,2.8,6.7,2.0,Iris-virginica\n6.3,2.7,4.9,1.8,Iris-virginica\n6.7,3.3,5.7,2.1,Iris-virginica\n7.2,3.2,6.0,1.8,Iris-virginica\n6.2,2.8,4.8,1.8,Iris-virginica\n6.1,3.0,4.9,1.8,Iris-virginica\n6.4,2.8,5.6,2.1,Iris-virginica\n7.2,3.0,5.8,1.6,Iris-virginica\n7.4,2.8,6.1,1.9,Iris-virginica\n7.9,3.8,6.4,2.0,Iris-virginica\n6.4,2.8,5.6,2.2,Iris-virginica\n6.3,2.8,5.1,1.5,Iris-virginica\n6.1,2.6,5.6,1.4,Iris-virginica\n7.7,3.0,6.1,2.3,Iris-virginica\n6.3,3.4,5.6,2.4,Iris-virginica\n6.4,3.1,5.5,1.8,Iris-virginica\n6.0,3.0,4.8,1.8,Iris-virginica\n6.9,3.1,5.4,2.1,Iris-virginica\n6.7,3.1,5.6,2.4,Iris-virginica\n6.9,3.1,5.1,2.3,Iris-virginica\n5.8,2.7,5.1,1.9,Iris-virginica\n6.8,3.2,5.9,2.3,Iris-virginica\n6.7,3.3,5.7,2.5,Iris-virginica\n6.7,3.0,5.2,2.3,Iris-virginica\n6.3,2.5,5.0,1.9,Iris-virginica\n6.5,3.0,5.2,2.0,Iris-virginica\n6.2,3.4,5.4,2.3,Iris-virginica\n5.9,3.0,5.1,1.8,Iris-virginica';
    var PARTIAL_IRIS_CSV = 'petal length, petal width, class\n1.4,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n1.3,0.2,Iris-setosa\n1.5,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n1.7,0.4,Iris-setosa\n1.4,0.3,Iris-setosa\n1.5,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n1.5,0.1,Iris-setosa\n1.5,0.2,Iris-setosa\n1.6,0.2,Iris-setosa\n1.4,0.1,Iris-setosa\n1.1,0.1,Iris-setosa\n1.2,0.2,Iris-setosa\n1.5,0.4,Iris-setosa\n1.3,0.4,Iris-setosa\n1.4,0.3,Iris-setosa\n1.7,0.3,Iris-setosa\n1.5,0.3,Iris-setosa\n1.7,0.2,Iris-setosa\n1.5,0.4,Iris-setosa\n1,0.2,Iris-setosa\n1.7,0.5,Iris-setosa\n1.9,0.2,Iris-setosa\n1.6,0.2,Iris-setosa\n1.6,0.4,Iris-setosa\n1.5,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n1.6,0.2,Iris-setosa\n1.6,0.2,Iris-setosa\n1.5,0.4,Iris-setosa\n1.5,0.1,Iris-setosa\n1.4,0.2,Iris-setosa\n1.5,0.1,Iris-setosa\n1.2,0.2,Iris-setosa\n1.3,0.2,Iris-setosa\n1.5,0.1,Iris-setosa\n1.3,0.2,Iris-setosa\n1.5,0.2,Iris-setosa\n1.3,0.3,Iris-setosa\n1.3,0.3,Iris-setosa\n1.3,0.2,Iris-setosa\n1.6,0.6,Iris-setosa\n1.9,0.4,Iris-setosa\n1.4,0.3,Iris-setosa\n1.6,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n1.5,0.2,Iris-setosa\n1.4,0.2,Iris-setosa\n4.7,1.4,Iris-versicolor\n4.5,1.5,Iris-versicolor\n4.9,1.5,Iris-versicolor\n4,1.3,Iris-versicolor\n4.6,1.5,Iris-versicolor\n4.5,1.3,Iris-versicolor\n4.7,1.6,Iris-versicolor\n3.3,1,Iris-versicolor\n4.6,1.3,Iris-versicolor\n3.9,1.4,Iris-versicolor\n3.5,1,Iris-versicolor\n4.2,1.5,Iris-versicolor\n4,1,Iris-versicolor\n4.7,1.4,Iris-versicolor\n3.6,1.3,Iris-versicolor\n4.4,1.4,Iris-versicolor\n4.5,1.5,Iris-versicolor\n4.1,1,Iris-versicolor\n4.5,1.5,Iris-versicolor\n3.9,1.1,Iris-versicolor\n4.8,1.8,Iris-versicolor\n4,1.3,Iris-versicolor\n4.9,1.5,Iris-versicolor\n4.7,1.2,Iris-versicolor\n4.3,1.3,Iris-versicolor\n4.4,1.4,Iris-versicolor\n4.8,1.4,Iris-versicolor\n5,1.7,Iris-versicolor\n4.5,1.5,Iris-versicolor\n3.5,1,Iris-versicolor\n3.8,1.1,Iris-versicolor\n3.7,1,Iris-versicolor\n3.9,1.2,Iris-versicolor\n5.1,1.6,Iris-versicolor\n4.5,1.5,Iris-versicolor\n4.5,1.6,Iris-versicolor\n4.7,1.5,Iris-versicolor\n4.4,1.3,Iris-versicolor\n4.1,1.3,Iris-versicolor\n4,1.3,Iris-versicolor\n4.4,1.2,Iris-versicolor\n4.6,1.4,Iris-versicolor\n4,1.2,Iris-versicolor\n3.3,1,Iris-versicolor\n4.2,1.3,Iris-versicolor\n4.2,1.2,Iris-versicolor\n4.2,1.3,Iris-versicolor\n4.3,1.3,Iris-versicolor\n3,1.1,Iris-versicolor\n4.1,1.3,Iris-versicolor\n6,2.5,Iris-virginica\n5.1,1.9,Iris-virginica\n5.9,2.1,Iris-virginica\n5.6,1.8,Iris-virginica\n5.8,2.2,Iris-virginica\n6.6,2.1,Iris-virginica\n4.5,1.7,Iris-virginica\n6.3,1.8,Iris-virginica\n5.8,1.8,Iris-virginica\n6.1,2.5,Iris-virginica\n5.1,2,Iris-virginica\n5.3,1.9,Iris-virginica\n5.5,2.1,Iris-virginica\n5,2,Iris-virginica\n5.1,2.4,Iris-virginica\n5.3,2.3,Iris-virginica\n5.5,1.8,Iris-virginica\n6.7,2.2,Iris-virginica\n6.9,2.3,Iris-virginica\n5,1.5,Iris-virginica\n5.7,2.3,Iris-virginica\n4.9,2,Iris-virginica\n6.7,2,Iris-virginica\n4.9,1.8,Iris-virginica\n5.7,2.1,Iris-virginica\n6,1.8,Iris-virginica\n4.8,1.8,Iris-virginica\n4.9,1.8,Iris-virginica\n5.6,2.1,Iris-virginica\n5.8,1.6,Iris-virginica\n6.1,1.9,Iris-virginica\n6.4,2,Iris-virginica\n5.6,2.2,Iris-virginica\n5.1,1.5,Iris-virginica\n5.6,1.4,Iris-virginica\n6.1,2.3,Iris-virginica\n5.6,2.4,Iris-virginica\n5.5,1.8,Iris-virginica\n4.8,1.8,Iris-virginica\n5.4,2.1,Iris-virginica\n5.6,2.4,Iris-virginica\n5.1,2.3,Iris-virginica\n5.1,1.9,Iris-virginica\n5.9,2.3,Iris-virginica\n5.7,2.5,Iris-virginica\n5.2,2.3,Iris-virginica\n5,1.9,Iris-virginica\n5.2,2,Iris-virginica\n5.4,2.3,Iris-virginica\n5.1,1.8,Iris-virginica';
    
    function make_input(name, value){
        html = '<div class="form-group">';
        html +='    <label for="param_'+name+'" class="col-lg-3 col-md-3 control-label">'+name+'</label>';
        html +='    <div class="col-lg-7 col-md-8">';
        html +='        <input type="text" class="form-control" id="param_'+name+'" name="param_'+name+'" placeholder="'+name+'" value="'+value+'" />';
        html +='    </div>';
        html +='</div>';
        return html;
    }
    
    function adjust_parameters(){
        current_classifier = $('#classifier').val();
        html = '';
        for (parameter in CLASSIFIERS[current_classifier]){
            html += make_input(parameter, CLASSIFIERS[current_classifier][parameter]);
        }
        $('#parameters').html(html);
    }
    
    $(document).ready(function(){
        // adjust_parameters
        adjust_parameters();
        
        // autosize
        $('textarea').autosize();
        
        // btn_default click
        $('#btn_complete_iris').click(function(){
            $('#training_csv').val(COMPLETE_IRIS_CSV).trigger('autosize.resize');
            event.preventDefault();
        });
        $('#btn_partial_iris').click(function(){
            $('#training_csv').val(PARTIAL_IRIS_CSV).trigger('autosize.resize');
            event.preventDefault();
        });
        
        // classifier change
        $('#classifier').change(function(){
            adjust_parameters();
        });
        
        // turn the form into ajax
        $('#classification-form').submit(function(e){
            form_data = $(this).serialize();
            form_url = $(this).attr('action');
            html = '<div class="alert alert-info">Processing, please wait</div>';
            $('#result').html(html);
            $.ajax({
                url : form_url,
                type: 'POST',
                data: form_data,
                timeout: 500000,
                dataType: 'json',
                success: function(response){
                    console.log(response);
                    var html = '';
                    if(!response.success){
                        html = '<div class="alert alert-danger"><b>ERROR</b> ' + response.message + '</div>';
                    }else{
                        html += '<h3>Classification Result :</h3>';
                        
                         // plot
                        if(response.draw_plot){
                            html += '<h4>Training And Testing Data Plot</h4>';
                            html += '<div class="well">';
                            html += '<p>per-2-dimensions plots. Data plot usually give better idea about classifier\'s behaviors, advantages, and weakneses</p>';
                            if(response.dimensions.length > 2){
                                html += '<div class="alert alert-warning"><b>Warning :</b> If your data contains more than 2 dimensions, please consider that the contour projection is probably inacurate</div>';
                            }
                            html += '<img style="width:90%" src="'+response.plot_url+'" />';
                            html += '</div>';
                        }
                        
                        // Accuracy and precision
                        rough_accuracy = 0.0;
                        for(i=0; i<response.groups.length; i++){
                            group = response.groups[i];
                            rough_accuracy += response.total_accuracy[group];
                        }
                        rough_accuracy /= response.groups.length;
                        rough_accuracy *= 100;
                        html += '<h4>Accuracy And Precision (Rough accuracy : '+rough_accuracy+'%)</h4>';
                        html += '<div class="well">';
                        html += '<p>We use several metrics to measure classifier\'s performance. For more information about those metrics, please visit <a target="blank" href="http://en.wikipedia.org/wiki/Accuracy_and_precision">http://en.wikipedia.org/wiki/Accuracy_and_precision</a></p>';
                        html += '<table class="table"><thead><tr><th colspan="2">Metric</th><th>Training</th><th>Testing</th><th>Total</th></tr></thead><tbody>';
                        var metrics = new Array('true_positive', 'true_negative', 'false_positive', 'false_negative', 'sensitivity', 'specificity', 'precision', 
                            'negative_predictive_value', 'accuracy', 'balanced_accuracy', 'informedness');
                        for (i=0; i<metrics.length; i++){
                            metric = metrics[i];
                            for (j=0; j<response.groups.length; j++){
                                group = response.groups[j];
                                if(j == 0){
                                    html += '<tr><td rowspan="' + response.groups.length + '">' + metric.replace(/_/gi, ' ') + '</td>';
                                }else{
                                    html += '<tr>';
                                }
                                html += '<td>' + group + '</td>';
                                html += '<td>' + response['training_'+metric][group] + '</td>';
                                html += '<td>' + response['testing_'+metric][group] + '</td>';
                                html += '<td>' + response['total_'+metric][group] + '</td>';
                                html += '</tr>';
                            }
                        }
                        html += '</tbody></table>';
                        html += '</div>';
                        
                        // prediction
                        if(response.do_prediction){
                            html += '<h4>Prediction</h4>';
                            html += '<div class="well">';
                            html += '<p>Prediction result</p>';
                            html += '<table class="table"><thead><tr>';
                            for(i=0; i<response.dimensions.length; i++){
                                dimension = response.dimensions[i];
                                html += '<th>'+dimension+'</th>';
                            }
                            html += '<th>Prediction</th>';
                            html += '</tr></thead><tbody>';
                            for(i=0; i<response.prediction_data.length; i++){
                                data = response.prediction_data[i];
                                result = response.prediction_result[i];
                                html += '<tr>';
                                for(j=0; j<response.dimensions.length; j++){
                                    html += '<td>'+data[j]+'</td>';
                                }
                                html += '<td>'+result+'</td></tr>';
                            }
                            html += '</tbody></table>';
                            html += '</div>';
                        }
                        
                       
                    }
                    $('#result').html(html);
                },
                error : function(){
                    html = '<div class="alert alert-danger"><b>AJAX Failed</b></div>';
                    $('#result').html(html);
                }
            });
            event.preventDefault();
        });
        
    });
</script>

%rebase('index/views/base', title='Classification')
