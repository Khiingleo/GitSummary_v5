$(document).ready(function () {
    $(".showContentBtn").click(function () {
        var url = $(this).data("url");
        toggleFileContent(url);
    });

    $(".exploreFolderBtn").click(async function () {
        var url = $(this).data("url");
        var listItem = $(this).closest('li');
        var nestedContents = listItem.find('.nestedContents');

        // Check if the folder contents are already loaded
        if (!nestedContents.data('contentsLoaded')) {
            try {
                await toggleFolderContents(url, nestedContents);
                nestedContents.data('contentsLoaded', true);
            } catch (error) {
                console.error('Error exploring folder:', error);
            }
        }

        // Toggle visibility of the nested contents
        nestedContents.toggle();
    });

    function toggleFileContent(url) {
        $.get(url)
            .done(function (content) {
                $("#fileContent").html('<pre>' + escapeHtml(content) + '</pre>');
            })
            .fail(function (error) {
                console.error('Error fetching file content:', error);
            });
    }

    function escapeHtml(html) {
        var text = document.createTextNode(html);
        var div = document.createElement('div');
        div.appendChild(text);
        return div.innerHTML;
    }

    async function toggleFolderContents(url, container) {
        try {
            // Clear existing content before fetching new content
            container.empty();

            var data = await fetchFolderContents(url);
            renderFolderContents(data, container);
        } catch (error) {
            console.error('Error fetching folder content:', error);
            throw error;
        }
    }

    function fetchFolderContents(url) {
        return new Promise(function (resolve, reject) {
            $.get(url)
                .done(function (data) {
                    resolve(data);
                })
                .fail(function (error) {
                    reject(error);
                });
        });
    }

    function renderFolderContents(data, container) {
        container.html('<h5>Folder Contents</h5><ul>');

        $.each(data, function (index, item) {
            var listItem = $('<li class="list-group">').appendTo(container);

            if (item.type === 'file') {
                listItem.append('<span>File: ' + item.name + '</span>');
                $('<button type="button" class="btn btn-outline-secondary">')
                    .text('Show Content')
                    .data('url', item.download_url)
                    .click(function () {
                        toggleFileContent(item.download_url);
                    })
                    .appendTo(listItem);
            } else if (item.type === 'dir') {
                listItem.append('<span>Folder: ' + item.name + '</span>');
                $('<button type="button" class="btn btn-outline-primary">')
                    .text('Explore Folder')
                    .data('url', item.url)
                    .click(async function () {
                        var nestedContents = $('<div class="nestedContents list-group-item" style="margin-left: 20px;"></div>').appendTo(listItem);
                        try {
                            await toggleFolderContents(item.url, nestedContents);
                        } catch (error) {
                            console.error('Error exploring subfolder:', error);
                        }
                    })
                    .appendTo(listItem);
            }
        });

        container.append('</ul>');
    }
});
