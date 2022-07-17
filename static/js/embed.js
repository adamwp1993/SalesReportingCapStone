!function embed(data) {
    let embedToken =  '{{ data.embed_token }}'
    let embedUrl = '{{ data.embed_url }}'
    let reportId = '{{ data.report_id }}'
    let loadedResolve, reportLoaded = new Promise((res, rej) => { loadedResolve = res; });
    let renderedResolve, reportRendered = new Promise((res, rej) => { renderedResolve = res; });
    // Get models. models contains enums that can be used.
    models = window['powerbi-client'].models;
    // We give All permissions to demonstrate switching between View and Edit mode and saving report.
    let permissions = models.Permissions.View;
    // Create the embed configuration object for the report
    // For more information see https://go.microsoft.com/fwlink/?linkid=2153590
    let config = {
        type: 'report',
        tokenType: models.TokenType.Embed,
        accessToken: embedToken,
        embedUrl: embedUrl,
        id: reportId,
        permissions: permissions,
        settings: {
            panes: {
                filters: {
                    visible: true
                },
                pageNavigation: {
                    visible: true
                }
            }
        }
    };
    // Get a reference to the embedded report HTML element
    let embedContainer = $('#reportContainer')[0];
    // Embed the report and display it within the div container.
    report = powerbi.embed(reportContainer, config);
    report.on("error", function (event) {
        console.log(event.detail);
    });
}