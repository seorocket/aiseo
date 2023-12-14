const socket = new WebSocket(`ws://${window.location.host}/ws/`);

socket.onmessage = function(event) {
    try {
        try {
            let data = JSON.parse(event.data),
                serialized_data = JSON.parse(data.serialized_data),
                type = data.type

            if (type === 'phrase') {
                let table_phrases = $('.project-item-section .phrases-item-table'),
                    table_tbody_phrases = $(table_phrases).find('tbody'),
                    block_phrases = $(table_tbody_phrases).find(`tr[data-id=${serialized_data[0].pk}]`),
                    count_data = 0,
                    resultWord;

                if ($(table_phrases).hasClass('main')) {
                    data.phrases_count_all === 1 ? resultWord = 'result' : resultWord = 'results';
                    count_data = data.phrases_count_all
                    if ($(block_phrases).length) {
                        $(block_phrases).fadeOut().find('td.status-td').text(serialized_data[0].fields.status_name)
                        $(block_phrases).fadeOut().fadeIn()
                    } else {
                        $(table_tbody_phrases).append(data.html_content_phrases)
                        block_phrases = $(`.project-item-section .phrases-item-table.main tbody tr[data-id=${serialized_data[0].pk}]`)
                        $(block_phrases).fadeOut().fadeIn()
                    }
                }
                $(`._titleBlock.${type}. .name`).text(`<span>${count_data}</span> ${resultWord} found`)
            }
            if (type === 'domain') {
                let table = $('.domainsSection .domains-table'),
                    table_tbody = $(`.domainsSection .domains-table tbody`),
                    block = $(`.domainsSection .domains-table tbody tr[data-id=${serialized_data[0].pk}]`),
                    domains_count_checked = data.domains_count_checked,
                    domains_count_timestamps = data.domains_count_timestamps,
                    domains_count_all = data.domains_count_all,
                    count_data = 0,
                    resultWord,
                    urlString = window.location.href,
                    url = new URL(urlString);

                if ($(table).hasClass('main')) {
                    if ($(block).length) {
                        $(block).fadeOut().find('td.status-td').text(serialized_data[0].fields.status_name)
                        $(block).fadeOut().fadeIn()
                        if (serialized_data[0].fields.status !== url.searchParams.get("status")) {
                            $(block).remove();
                            count_data = Number($(`._titleBlock.${type} .name > span`).text())
                            count_data--
                            count_data === 1 ? resultWord = 'result' : resultWord = 'results';
                            $(`._titleBlock.${type} .name`).text(`<span>${count_data}</span> ${resultWord} found`)
                        }
                    } else {
                        if (!url.searchParams.size) {
                            domains_count_all === 1 ? resultWord = 'result' : resultWord = 'results';
                            count_data = domains_count_all
                            $(table_tbody).append(data.html_content_domains)
                            block = $(`.domainsSection .domains-table.main tbody tr[data-id=${serialized_data[0].pk}]`)
                            $(block).fadeOut().fadeIn()
                            $(`._titleBlock.${type} .name`).text(`<span>${count_data}</span> ${resultWord} found`)
                        }
                    }
                } else if ($(table).hasClass('timestamps')) {
                    domains_count_timestamps === 1 ? resultWord = 'result' : resultWord = 'results';
                    count_data = domains_count_timestamps
                    if ($(block).length) {
                        if (String(serialized_data[0].fields.status) !== '6') {
                            if (serialized_data[0].fields.status !== url.searchParams.get("status")) {
                                $(block).remove();
                                count_data = Number($(`._titleBlock.${type} .name > span`).text())
                                count_data--
                                count_data === 1 ? resultWord = 'result' : resultWord = 'results';
                                $(`._titleBlock.${type} .name`).text(`<span>${count_data}</span> ${resultWord} found`)
                            }
                        }
                    } else {
                        if (String(serialized_data[0].fields.status) === '6') {
                            if (!url.searchParams) {
                                domains_count_all === 1 ? resultWord = 'result' : resultWord = 'results';
                                count_data = domains_count_all
                                $(table_tbody).append(data.html_content_domains)
                                block = $(`.domainsSection .domains-table.timestamps tbody tr[data-id=${serialized_data[0].pk}]`)
                                $(block).fadeOut().fadeIn()
                                $(`._titleBlock.${type} .name`).text(`<span>${count_data}</span> ${resultWord} found`)
                            }
                        }
                    }
                }
            }
        } catch (error) {
            // console.log(event.data)
        }
    } catch (e) {
        console.log('Error:', e.message);
    }
};