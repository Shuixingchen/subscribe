import scrapy
import json


class XrequestSpider(scrapy.Spider):
    name = "xrequest"
    allowed_domains = ["x.com"]
    start_urls = ["https://x.com"]

    def start_requests(self):
        url = 'https://x.com/i/api/graphql/BjT3MvG1CwfTuJxTLX4ovg/CreateTweet'
        headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,en-GB;q=0.6',
        'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'guest_id=v1%3A171013361575518595; night_mode=2; guest_id_marketing=v1%3A171013361575518595; guest_id_ads=v1%3A171013361575518595; kdt=GDQ2CSYvpCM2SrKc6RoW4iPd7xq80XRBbcNFa3Vq; auth_token=7c8e5aef21b16e89ecd27433b072202044fecc4b; ct0=22524b4d1354e4a9da795f0a7a77d84e9079eb9cd40a44a47da45a154d7b7b6d99fa1b8b357c64ab6bbb4f037828b40e34e327a0cad879e03add55c62acaa69becd77141fb238c9e4eb46524cd96a804; twid=u%3D387468163; _monitor_extras={"deviceId":"jfs_WOAtw5PoLjLAPOsegt","eventId":2,"sequenceNumber":2}; personalization_id="v1_RUaRtnUybjrmpkdaE4LKmg=="; lang=zh-cn; external_referer=8e8t2xd8A2w%3D|0|F8C7rVpldvGNltGxuH%2ByoRY%2FzjrflHIZH061f%2B5OiIwP17ZTz34ZGg%3D%3D; amp_56bf9d=2c1ca069-e580-43d5-afe5-4b9892c8270a...1ifei6h83.1ifeik7pi.6.i.o',  # 添加其他Cookie信息
        'origin': 'https://x.com',
        'pragma': 'no-cache',
        'referer': 'https://x.com/compose/post',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-client-transaction-id': '6wkkJI5oaNzmV3uNcucELCsDuKD+H224ktMCt4Z9c0Bpl6GaMx/2GFJK2aCaKOaj1tyR/+h9IkoBh8DQcr4IJ0WAw9rd6A',
        'x-client-uuid': 'b1ccce64-ae34-48a4-bf3d-bee6c1cd33cf',
        'x-csrf-token': '22524b4d1354e4a9da795f0a7a77d84e9079eb9cd40a44a47da45a154d7b7b6d99fa1b8b357c64ab6bbb4f037828b40e34e327a0cad879e03add55c62acaa69becd77141fb238c9e4eb46524cd96a804',
        'x-twitter-active-user': 'yes',
        'x-twitter-auth-type': 'OAuth2Session',
        'x-twitter-client-language': 'zh-cn',
        }

        data = '{"variables":{"tweet_text":"always going down","dark_request":false,"media":{"media_entities":[],"possibly_sensitive":false},"semantic_annotation_ids":[],"disallowed_reply_options":null},"features":{"premium_content_api_read_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"responsive_web_grok_analyze_button_fetch_trends_enabled":false,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"profile_label_improvements_pcf_label_in_post_enabled":false,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"articles_preview_enabled":true,"rweb_video_timestamps_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_enhance_cards_enabled":false},"queryId":"BjT3MvG1CwfTuJxTLX4ovg"}'

        yield scrapy.Request(url, method='POST', headers=headers, body=data, callback=self.parse)

    def parse(self, response):
        content = response.json()
        print("body: ",content)