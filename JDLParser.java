import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch.core.SearchRequest;
import org.opensearch.client.opensearch.core.search.*;
import org.opensearch.index.query.QueryBuilders;
import org.opensearch.index.query.ExistsQueryBuilder;
import org.opensearch.index.query.TermQueryBuilder;

// Assuming 'client' is your instance of OpenSearchClient
OpenSearchClient client = ...;

SearchRequest searchRequest = new SearchRequest.Builder()
    .index("your_index_name") // Set the index you want to search
    .source(new SearchSourceBuilder()
        .query(QueryBuilders.boolQuery()
            .must(new TermQueryBuilder("value_rent", "gg"))
            .filter(new ExistsQueryBuilder("value_rent")))
        .size(1)
        .trackTotalHits(false)
        .terminateAfter(1))
    .build();

// Execute the search
SearchResponse<?> searchResponse = client.search(searchRequest, YourDocumentClass.class);