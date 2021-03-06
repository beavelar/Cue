import express from 'express';
import { DBStore } from 'src/store/db-store';
import { Logger } from '../util/logging/logger';

export class Historical {
  /** The express router to utilize for the routes */
  public router: express.Router = express.Router();

  constructor(private readonly logger: Logger, private readonly store: DBStore) {
    /**
     * The callback for DB-Store historical GET request. Will create a request to get the data in the historical
     * collection in the database.
     */
    this.router.get('/', (req, res) => {
      this.logger.info('historical', `Receive GET request`);
      this.store.getAllHistorical().then((data) => {
        this.logger.info('historical', 'Successfully retrieved historical data from the database');
        res.status(200).json(data);
      }).catch((err) => {
        this.logger.critical('historical', 'An error occurred retrieving historical data from the database', err);
        res.status(500).json(err);
      });
    });

    /**
     * The callback for DB-Store historical GET request with a start parameter. Will create a request to get the
     * data in the historical collection in the database.
     */
    this.router.get('/:start', (req, res) => {
      this.logger.info('historical', `Receive GET request with start: ${req.params.start}`);
      const startSeconds = parseInt(req.params.start);
      if (!isNaN(startSeconds)) {
        this.store.getHistoricalAlertDate(startSeconds).then((data) => {
          this.logger.info('historical', 'Successfully retrieved historical data from the database');
          res.status(200).json(data);
        }).catch((err) => {
          this.logger.critical('historical', 'An error occurred retrieving historical data from the database', err);
          res.status(500).json(err);
        });
      }
      else {
        const message = `Invalid start parameter provided: ${req.params.start}`;
        this.logger.warning('historical', message);
        res.status(500).json(message);
      }
    });

    /**
     * The callback for DB-Store historical GET request with a start and stop parameter. Will create a request to
     * get the data in the historical collection in the database.
     */
    this.router.get('/:start/:stop', (req, res) => {
      this.logger.info('historical', `Receive GET request with start: ${req.params.start} and stop: ${req.params.stop}`);
      const startSeconds = parseInt(req.params.start);
      const stopSeconds = parseInt(req.params.stop);
      if (!isNaN(startSeconds) && !isNaN(stopSeconds)) {
        this.store.getHistoricalAlertDate(startSeconds, stopSeconds).then((data) => {
          this.logger.info('historical', 'Successfully retrieved historical data from the database');
          res.status(200).json(data);
        }).catch((err) => {
          this.logger.critical('historical', 'An error occurred retrieving historical data from the database', err);
          res.status(500).json(err);
        });
      }
      else {
        const message = `Invalid start or stop parameter provided: start - ${req.params.start}, stop - ${req.params.stop}`;
        this.logger.warning('historical', message);
        res.status(500).json(message);
      }
    });

    /**
     * The callback for DB-Store historical POST request. Will create a request to write the incoming data to
     * the historical collection in the database.
     */
    this.router.post('/', (req, res) => {
      this.logger.info('historical', `Receive POST request`);
      this.store.writeHistorical(req.body).then((result) => {
        this.logger.info('historical', 'Successfully wrote historical data to the database');
        res.status(200).json(result);
      }).catch((err) => {
        this.logger.critical('historical', 'An error occurred writing historical data to the database', err);
        res.status(500).json(err);
      });
    });

    /**
     * The callback for DB-Store historical DELETE request. Will create a request to delete the data in the
     * historical collection in the database.
     */
    this.router.delete('/', (req, res) => {
      this.logger.info('historical', `Receive DELETE request`);
      this.store.deleteAllHistorical().then((result) => {
        this.logger.info('historical', 'Successfully deleted historical data from the database');
        res.status(200).json(result);
      }).catch((err) => {
        this.logger.critical('historical', 'An error occurred deleting historical data from the database', err);
        res.status(500).json(err);
      });
    });
  }
}