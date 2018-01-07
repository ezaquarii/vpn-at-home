export const selectFeatures = function(state) {

    const features = {
        can_create_client: false,
        can_create_server: false,
        can_set_settings: false,
        can_send_emails: false,
        is_authenticated: false,
    };

    const is_superuser = state.account.permissions.has("superuser");
    const has_servers = state.servers.length !== 0;

    features.can_create_server = !has_servers && is_superuser;
    features.can_create_client = has_servers;
    features.can_set_settings = state.account.permissions.has("superuser");
    features.can_send_emails = window.django.email_enabled;
    features.is_authenticated = state.account.is_logged_in;

    return features;
};
